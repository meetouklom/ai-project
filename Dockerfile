# ใช้ Nginx สำหรับรันหน้าเว็บ HTML/JS
FROM nginx:alpine

# คัดลอกไฟล์เว็บของเราเข้าไปในเซิร์ฟเวอร์ Nginx
COPY . /usr/share/nginx/html

# เปิดพอร์ต 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]