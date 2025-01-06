from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import UserDetail
from .serializers import UserDetailSerializer
from django.core.exceptions import ObjectDoesNotExist
from UserApp import serializers

class UserSignupView(APIView):
    """
    API endpoint for user registration. 
    Validates for duplicate entries based on username, phone_number, and email.
    """

    def post(self, request):
        try:
            serializer = UserDetailSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "User registered successfully."},
                    status=status.HTTP_201_CREATED
                )
            
            return Response(
                {"errors": serializer.errors, "message": "Validation failed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except serializers.ValidationError as e:
            return Response(
                {"error": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class SearchCommonUsersView(APIView):
    """
    API endpoint to search for users with matching phone number or email.
    
    POST:
    - Accepts: phone_number (optional), email (optional) through form-data or request body.
    - Returns: List of users with matching phone or email.
    - Why POST instead of GET?:
        - To avoid exposing sensitive information like phone numbers in the URL.
    
    If both phone_number and email are missing, the API returns a 400 error.
    """
    
    def post(self, request):
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')

        # Sanity check for query parameters
        if not phone_number and not email:
            return Response(
                {"error": "Please provide either phone_number or email for search."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch users based on phone or email match
            users = UserDetail.find_common_users(phone_number, email)
            
            if not users.exists():
                return Response(
                    {"message": "No users found with matching details."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Serialize and return matching users
            serializer = UserDetailSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            # Handle case when no object exists (fallback)
            return Response(
                {"message": "No matching records found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        except ValidationError as e:
            # Handle Django model validation errors
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            # Catch unexpected errors to prevent server crash
            return Response(
                {"error": "An error occurred while processing the request.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )