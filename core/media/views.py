from rest_framework.views import APIView
from rest_framework.response import Response
from core.base.viewsets import SuperReadOnlyModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Media
from .serializers import MediaSerializer
from django.contrib.contenttypes.models import ContentType
from rest_framework.parsers import MultiPartParser, FormParser
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class FileUploadView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        # التحقق من وجود ملفات في الطلب
        if "file" not in request.FILES:
            return Response(
                "لم يتم تقديم أي ملفات.", status=status.HTTP_400_BAD_REQUEST
            )

        files = request.FILES.getlist("file")

        if not files:
            return Response(
                "لم يتم تقديم أي ملفات.", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # الحصول على اسم الموديل لاستخدامه في مسار التحميل
            model_name = request.POST.get(
                "model_name", "global"
            )  # القيمة الافتراضية 'global' إذا لم يتم توفيرها

            media_ids = []

            for file_obj in files:
                # إنشاء كائن Media لكل ملف
                media = Media(file=file_obj, file_type=file_obj.content_type)

                # تعيين الخاصية المؤقتة 'custom_upload_path'
                media.custom_upload_path = model_name  # استخدام اسم الموديل كاسم المجلد

                # حفظ كائن Media
                media.save()

                # جمع معرفات الميديا
                media_ids.append({"id": media.pk, "url": media.file.url})

            # إرجاع قائمة بمعرفات الميديا كاستجابة JSON
            return Response(media_ids, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                "فشل في رفع الملفات.", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LinkImageView(APIView):
    def post(self, request):
        image_id = request.data.get("image_id")
        app_name = request.data.get("app_name", "products")
        model_name = request.data.get("model_name")
        field_name = request.data.get("field_name")
        field_value = request.data.get("field_value")

        if not image_id or not model_name or not field_name or not field_value:
            return Response(
                {"error": "يجب تقديم image_id، model_name، field_name، و field_value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # الحصول على الصورة
        try:
            media = Media.objects.get(id=image_id)
        except Media.DoesNotExist:
            return Response(
                {"error": "الصورة غير موجودة."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            ModelClass = apps.get_model(app_name, model_name)
        except LookupError:
            return Response(
                {"error": f"النموذج '{model_name}' غير موجود."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # البحث عن الكائن المناسب
        if field_name == "barcodes":
            object_filters = {field_name: [f"{field_value}"]}
        else:
            object_filters = {field_name: field_value}
        try:
            obj = ModelClass.objects.get(**object_filters)
        except ModelClass.DoesNotExist:
            return Response(
                {
                    "error": f"لم يتم العثور على {model_name} بقيمة {field_value} في الحقل {field_name}."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": f"خطأ في البحث عن {model_name}: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ربط الصورة بالكائن
        if hasattr(obj, "images"):
            obj.images.add(media)
            # تحديث الصورة الافتراضية إذا كان الحقل موجودًا
            if hasattr(obj, "default_image"):
                obj.default_image = media.file.url
            obj.save()
            return Response(
                {"message": f"تم ربط الصورة بـ {model_name} وتحديث الصورة الافتراضية."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": f"النموذج {model_name} لا يحتوي على حقل 'images'."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CheckObjectExistenceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        app_name = request.data.get("app_name", "products")
        model_name = request.data.get("model_name")
        field_name = request.data.get("field_name")
        field_value = request.data.get("field_value")

        if not model_name or not field_name or not field_value:
            return Response(
                {"error": "model_name, field_name, and field_value are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ModelClass = apps.get_model(app_name, model_name)

        except LookupError:
            return Response(
                {"error": f"Model '{model_name}' does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if field_name == "barcodes":
            object_filters = {field_name: [f"{field_value}"]}
        else:
            object_filters = {field_name: field_value}
        try:
            obj = ModelClass.objects.get(**object_filters)
            return Response({"message": "Object exists."}, status=status.HTTP_200_OK)
        except ModelClass.DoesNotExist:
            return Response(
                {"error": "Object does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error checking object existence: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MediaViewSet(SuperReadOnlyModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
