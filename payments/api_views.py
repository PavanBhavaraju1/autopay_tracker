from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Card, Subscription
from .serializers import PopupSubscriptionSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_from_popup(request):
    serializer = PopupSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        # Create or get card
        card, created = Card.objects.get_or_create(
            name=serializer.validated_data['card_name'],
            last4=serializer.validated_data['card_last4'],
            defaults={'issuer': '', 'is_active': True}
        )
        
        # Create subscription
        subscription = Subscription.objects.create(
            card=card,
            service_name=serializer.validated_data['service_name'],
            amount=serializer.validated_data['amount'],
            next_billing_date=serializer.validated_data['next_billing_date'],
            status=serializer.validated_data['status']
        )
        
        return Response({
            'message': 'Subscription saved!',
            'subscription_id': subscription.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
