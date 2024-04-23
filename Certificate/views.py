from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Certificate
from .serializer import CertificateSerializer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Image, Spacer, SimpleDocTemplate
from reportlab.lib.units import inch
from io import BytesIO
from pdf2image import convert_from_bytes
from django.core.files.base import ContentFile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CertificateAPI(APIView):
            
    permission_classes = [IsAuthenticated]  # Requires users to be authenticated
    authentication_classes = [TokenAuthentication]  
    def post(self, request):

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        request.data.user=request.user
        print(request.data.user)
        serializer = CertificateSerializer(data=request.data)
        print(request.data.user)

        if serializer.is_valid():
            certificate = serializer.save(user=request.user)
            
    
            certificate.user = request.user
            certificate.save()

            pdf = self.generate_pdf(certificate)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{certificate.username}-certificate.pdf"'
            return response
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        # Retrieve all certificates for the logged-in user
        certificates = Certificate.objects.filter(user=request.user)
        # Serialize the data
        serializer = CertificateSerializer(certificates, many=True)
        # Return the serialized data
        return Response(serializer.data,status=status.HTTP_200_OK)

    def generate_pdf(self, certificate):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Draw the background image
        image_path = 'static/images/image.png'
        p.drawImage(image_path, 0, 0, width=600, height=820, mask='auto')

        # Text settings
        p.setFont("Helvetica", 18)
        text_x = 300  # Center horizontally
        text_y = 410  # Center vertically, adjust as needed

        # Draw the text
        p.drawCentredString(text_x, text_y+10, f"Congratulations, {certificate.username}!")
        p.drawCentredString(text_x, text_y - 30, "You have successfully completed the course:")
        p.drawCentredString(text_x, text_y - 50, certificate.course_name)
        p.drawCentredString(text_x-130, text_y - 200, f"Issued on: {certificate.date_of_issue.strftime('%B %d, %Y')}")

        # Finalize the PDF
        p.showPage()
        p.save()
        buffer.seek(0)

        # Convert the first page of the PDF to an image
        images = convert_from_bytes(buffer.getvalue())
        image = images[0]
        image_io = BytesIO()
        image.save(image_io, format='PNG')
        image_content_file = ContentFile(image_io.getvalue())
        
        # Save the image to the Certificate model's ImageField
        certificate.certificate_image.save(f'{certificate.username}_certificate.png', image_content_file)
        

        return buffer.getvalue()
    

