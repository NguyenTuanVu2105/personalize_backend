from rest_framework.response import Response

from HUB.services.model_service import get_model_related_fields, AGGREGATE_FUNCTION_DICT
from HUB.viewsets.base import AdminGenericAPIView
from notification.services.notification import send_custom_email, send_seller_custom_email_task
from user.models import User


class SellerEmailSupportedAggregate(AdminGenericAPIView):
    def get(self, request):
        return Response({"supported_agg": list(AGGREGATE_FUNCTION_DICT.keys())})


class SellerEmail(AdminGenericAPIView):
    def post(self, request):
        request_data = request.data
        all_emails = User.objects.values_list('email', flat=True)
        if not request_data.get('send_to_all_user'):
            receiver_emails = request_data['receiver_emails']
            if not all([email in all_emails for email in receiver_emails]):
                return Response({'success': False, 'message': 'Email not existed'})
        else:
            receiver_emails = all_emails
        if not receiver_emails:
            return Response({'success': False, 'message': 'No email selected'})
        content = request_data['content']
        subject = request_data['subject']
        data_mapping = request_data.get('data_mapping') or {'subject': {}, 'content': {}}
        n_emails_limit = 100
        for i in range(0, len(receiver_emails), n_emails_limit):
            send_seller_custom_email_task.delay(
                receiver_emails=receiver_emails[i:min(i + n_emails_limit, len(receiver_emails))],
                subject=subject,
                content=content, data_mapping=data_mapping)
        return Response({'success': True, 'emails': receiver_emails})
