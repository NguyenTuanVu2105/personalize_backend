import logging
import re
from datetime import datetime

from django.db.models import Q
from django.utils import timezone
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from HUB.exceptions.FormValidationError import FormValidationError
from HUB.paginations import EnhancedPageNumberPagination
from HUB.services.chunk_cloud_storage_uploader import ChunkCloudStorageUploader
from HUB.viewsets.base import AuthenticatedGenericViewSet
from HUB.viewsets.mixins.search_mixins import SearchableListModelMixin
from user.queries import RawSearchQuery
from user_product.constants import ArtworkStatus
from user_product.functions import create_artwork_history, update_fulfill_artwork
from user_product.models import Artwork, ArtworkDefault
from ..filters import ArtworkFilter
from ..functions.update_artwork import deactivate_artworks, activate_artworks
from ..paginations import ArtworkPagination
from ..serializers import ArtworkSerializer
from ..services.artwork import update_artwork
from rest_framework import permissions

logging.basicConfig()
logger = logging.getLogger(__name__)
value_list = ['id', 'name', "owner", 'file_url', 'is_public', 'status', 'width', 'height', 'last_used_time',
              'update_time',
              'create_time', 'total_created_product', "is_default", "is_legal_accepted"]


# value_list = ["id", "name", "owner"]


class ArtworkViewSet(SearchableListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     AuthenticatedGenericViewSet):
    queryset = Artwork.objects.all().select_related("owner").order_by('-create_time')
    permission_classes = [permissions.AllowAny]
    serializer_class = ArtworkSerializer
    pagination_class = ArtworkPagination
    filterset_class = ArtworkFilter
    ordering_fields = ['id', 'owner', 'name', 'file_url', 'is_public', 'last_used_time']

    error_messages = {
        "file": {
            "error": "Upload file error"
        }
    }

    def get_queryset(self, q=None, status=None):
        if q:
            q = re.sub(r'[!\'()|&<>:*\[\];$\"]', ' ', q).strip()
            q = re.sub(r'\s+', ' & ', q)
            if q.strip():
                q += ':*'
                self.queryset = self.get_queryset().filter(tsv_metadata_search=RawSearchQuery(q))
        if status:
            self.queryset = self.get_queryset().filter(status=status)
        # return self.queryset.filter(owner=self.request.user.pk).exclude(status=ArtworkStatus.UPLOADED)
        return self.queryset.filter(Q(owner_id='12079083658273')).exclude(
            status__in=[ArtworkStatus.UPLOADED, ArtworkStatus.AD_CLONED, ArtworkStatus.ERROR, ArtworkStatus.SP_CLONED])

    def get_default_artwork_queryset(self, q=None):
        artwork_default = ArtworkDefault.objects.filter(status=ArtworkStatus.ACTIVE)
        if q:
            q = re.sub(r'[!\'()|&<>:*\[\];$\"]', ' ', q).strip()
            q = re.sub(r'\s+', ' & ', q)
            if q.strip():
                q += ':*'
                return artwork_default.filter(tsv_metadata_search=RawSearchQuery(q))
        return artwork_default

    @action(methods=["GET"], detail=False, url_path="list_with_default", permission_classes=[permissions.AllowAny])
    def list_with_default(self, request, *args, **kwargs):
        request_data = request.query_params
        q = request.query_params.get("q")

        artwork_default = self.get_default_artwork_queryset(q).values(*value_list)

        paginator = EnhancedPageNumberPagination()
        page = paginator.paginate_queryset(artwork_default, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


    @action(methods=["GET"], detail=False, url_path="default", permission_classes=[permissions.AllowAny])
    def default(self, request, *args, **kwargs):
        request_data = request.query_params
        side_id = request_data.get("side_id")
        # status = request_data.get("status")
        q = request.query_params.get("q")

        # artwork_queryset = self.get_queryset(q, status).order_by("-last_used_time")
        # artwork_default_used = [x for x in artwork_queryset.values_list("artwork_default_id", flat=True) if
        #                         x is not None]
        artwork_default = self.get_default_artwork_queryset(q).filter(
            product_side_id=side_id).values(*value_list)

        # artwork_queryset = artwork_queryset.values(*value_list).union(artwork_default).order_by("-last_used_time")
        paginator = EnhancedPageNumberPagination()
        page = paginator.paginate_queryset(artwork_default, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        artwork = self.get_object()
        old_name = artwork.name
        is_new_artwork_file = request.POST.get('is_new_artwork_file')
        name = request.POST.get('name')
        if is_new_artwork_file:
            # logger.info("Save new artwork...")
            resumable_total_chunks = int(request.POST.get('total'))
            resumable_file_name = request.POST.get('file_name')
            start_millis_timestamp = int(timezone.now().timestamp() * 1000)
            if ChunkCloudStorageUploader.all_uploaded(resumable_file_name, resumable_total_chunks):
                merged_file = ChunkCloudStorageUploader.merge_chunks(resumable_file_name, resumable_total_chunks)
                artwork = update_artwork(artwork, resumable_file_name, name, merged_file)
            else:
                raise FormValidationError(field="file", code="error")
            create_artwork_history(artwork.id, old_name, artwork.file_url, artwork.width,
                                   artwork.height, artwork.sha256)
            # logger.info("----------- total time for updating: {}".format(
            #     (int(timezone.now().timestamp() * 1000) - start_millis_timestamp) / 1000))
        elif name and old_name != name:
            artwork.name = name
            artwork.save()
        # logger.info("UPDATE ARTWORK IN FULFILL...")
        if is_new_artwork_file:
            update_fulfill_artwork.delay(artwork.id)
        res = ArtworkSerializer(instance=artwork).data
        res["status"] = "FINISHED"
        return Response({"success": True, "data": res})

    def destroy(self, request, *args, **kwargs):
        request.data["ids"] = [kwargs['pk']]
        response = self.bulk_update_artworks_status(request=request, handle_function=deactivate_artworks)
        return response

    @action(methods=["PUT"], detail=True, url_path="activate")
    def activate(self, request, *args, **kwargs):
        request.data["ids"] = [kwargs['pk']]
        response = self.bulk_update_artworks_status(request=request, handle_function=activate_artworks)
        return response

    @action(methods=["PUT"], detail=False, url_path="bulk-active")
    def bulk_active(self, request, *args, **kwargs):
        response = self.bulk_update_artworks_status(request=request, handle_function=activate_artworks)
        return response

    @action(methods=["DELETE"], detail=False, url_path="bulk-deactive")
    def bulk_destroy(self, request, *args, **kwargs):
        response = self.bulk_update_artworks_status(request=request, handle_function=deactivate_artworks)
        return response

    @action(methods=["POST"], detail=False, url_path="clone_default")
    def clone_default_artwork(self, request, *args, **kwargs):
        artwork_default_id = request.data.get("default_id")
        artwork_default = ArtworkDefault.objects.get(id=artwork_default_id)
        artwork, created = Artwork.objects.get_or_create(artwork_default_id=artwork_default.id,
                                                         status=ArtworkStatus.AD_CLONED,
                                                         owner_id=request.user.pk,
                                                         defaults={
                                                             "name": artwork_default.name,
                                                             "original_image_path": artwork_default.original_image_path,
                                                             "thumbnail_image_path": artwork_default.thumbnail_image_path,
                                                             "file_url": artwork_default.file_url,
                                                             "sha256": artwork_default.sha256,
                                                             "width": artwork_default.width,
                                                             "height": artwork_default.height,
                                                             "last_used_time": datetime.utcnow(),
                                                             "is_legal_accepted": True
                                                         })
        return Response({"success": True, "data": self.get_serializer(artwork).data})

    def bulk_update_artworks_status(self, request, handle_function):
        artwork_ids = request.data.get("ids", [])
        artwork_ids = self.get_queryset().filter(id__in=artwork_ids).values_list("id", flat=True)
        success = False
        if len(artwork_ids) > 0:
            try:
                updated_row_count = handle_function(self.queryset, artwork_ids)
            except Exception as e:
                logger.exception(e)
            else:
                if updated_row_count > 0:
                    success = True
        return Response({"success": success})

    @action(methods=["POST"], detail=True, url_path="clone")
    def clone_user_artwork(self, request, *args, **kwargs):
        request_data = request.data
        user_id = request.user.pk
        sha256 = request_data.get('sha256')
        artwork = Artwork.objects.get(pk=kwargs['pk'])

        if sha256:
            if sha256 == artwork.sha256 and artwork.owner_id != user_id:
                try:
                    artwork, created = Artwork.objects.get_or_create(sha256=sha256,
                                                                     owner_id=user_id,
                                                                     defaults={
                                                                         "status": ArtworkStatus.SP_CLONED,
                                                                         "name": artwork.name,
                                                                         "original_image_path": artwork.original_image_path,
                                                                         "thumbnail_image_path": artwork.thumbnail_image_path,
                                                                         "file_url": artwork.file_url,
                                                                         "width": artwork.width,
                                                                         "height": artwork.height,
                                                                         "last_used_time": datetime.utcnow(),
                                                                         "is_legal_accepted": True
                                                                     })
                except Artwork.MultipleObjectsReturned as e:
                    artwork = Artwork.objects.filter(sha256=sha256, owner_id=user_id).first()
                return Response(
                    {"success": True, "artwork_id": artwork.id, "is_legal_accepted": artwork.is_legal_accepted})

            elif artwork.owner_id == user_id:
                return Response(
                    {"success": True, "artwork_id": artwork.id, "is_legal_accepted": artwork.is_legal_accepted})

            else:
                return Response({"success": False, "artwork_id": None})

        elif not sha256:
            artwork = Artwork.objects.create(owner_id=user_id,
                                             status=ArtworkStatus.SP_CLONED,
                                             name=artwork.name,
                                             original_image_path=artwork.original_image_path,
                                             thumbnail_image_path=artwork.thumbnail_image_path,
                                             file_url=artwork.file_url,
                                             width=artwork.width,
                                             height=artwork.height,
                                             last_used_time=datetime.utcnow(),
                                             is_legal_accepted=True)

            return Response({"success": True, "artwork_id": artwork.id, "is_legal_accepted": artwork.is_legal_accepted})

    @action(methods=['PUT', 'PATCH'], detail=True, url_path='force-activate')
    def force_activate(self, request, *args, **kwargs):
        artwork = Artwork.objects.get(id=kwargs['pk'])
        artwork.status = ArtworkStatus.ACTIVE
        artwork.name = request.data.get('name') or artwork.name
        artwork.save()
        return Response({'success': True, 'artwork': self.get_serializer(artwork).data})
