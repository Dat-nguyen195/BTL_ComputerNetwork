"""Place detailed evidence in the relevant report chapters instead of appendices."""
import re
from pathlib import Path
NAMES=('wan-cisco','main-cisco','aux-cisco','gpon-cisco','security-cisco','wifi-cisco','mpls-cisco','vpn-cisco','layers-cisco','camera-cisco')
def integrate(text):
 sections=re.split(r'(?m)^# Phụ lục ',text)
 body=sections[0]
 blocks={s[0]:s.split('\n',1)[1].replace('\\clearpage','') for s in sections[1:]}
 def nest(s):return re.sub(r'(?m)^(#{1,5}) ',lambda m:'#'*(len(m[1])+1)+' ',s)
 def before(marker,title,content):
  nonlocal body
  body=body.replace(marker,'## '+title+'\n\n'+nest(content)+'\n\n'+marker,1)
 before('## Server Farm, DMZ','Bảng địa chỉ chi tiết và ma trận truy cập',blocks.get('C',''))
 before('## Đọc kết quả và tái lập','Kết quả đo và bằng chứng các lần chạy',blocks.get('A','')+'\n'+blocks.get('G',''))
 before('## Đọc kết quả và tái lập','Kịch bản demo và đối chứng',blocks.get('F','').split('## Chọn file nộp')[0])
 before('# Tài liệu tham khảo','Tái lập và danh mục bàn giao',blocks.get('B',''))
 replacements={'phụ lục A':'mục kết quả đo trong chương 3','phụ lục G':'mục kiểm tra ngày 05/11/2026 trong chương 3','phụ lục C':'bảng địa chỉ chi tiết trong chương 2','phụ lục bằng chứng':'mục kết quả đo trong chương 3','Phụ lục A':'Mục kết quả đo','Phụ lục G':'Mục kiểm tra ngày 05/11/2026'}
 for a,b in replacements.items():body=body.replace(a,b)
 figures=[('wan-cisco','### Kiến trúc kết nối ba cơ sở','Sơ đồ logic ba cơ sở: định tuyến WAN, Internet tập trung và DMZ.'),('main-cisco','### Tổ chức MDF, IDF','Phân bố IDF theo tầng tại Main và hai đường uplink dự trù.'),('aux-cisco','### Phương án hybrid GPON','Thiết kế vật lý dùng chung cho mỗi cơ sở DBP/BHTQ.'),('gpon-cisco','### Băng thông và ngân sách quang','GPON hành chính: OLT, splitter, ONT và phạm vi VLAN60.'),('wifi-cisco','### Hệ thống giám sát camera','Phân vùng Wi-Fi nhân viên, khách và camera ghi local.'),('security-cisco','### Phân vùng và quyền tối thiểu','Các vùng bảo mật và quyền truy cập; hình lược bỏ Edge để nhấn mạnh chính sách.'),('vpn-cisco','### IDS/IPS và chống phishing','Hai phương án VPN đề xuất, chưa có bằng chứng triển khai crypto.'),('mpls-cisco','## Quy trình cấu hình','Module MPLS L3VPN riêng: vai trò P, PE, CE và các mạng LAN.')]
 for name,marker,caption in figures:
  idx=body.find(marker)
  if idx>=0:body=body[:idx]+f'![{caption}](../latex/assets/{name}.pdf){{width=100%}}\n\n'+body[idx:]
 # The physical figures already appear with Cisco details in chapter 2.
 for name,marker,caption in [('layers-cisco','### Phân tầng và vùng tải cao','So sánh ba tầng chức năng tại Main và hai tầng tại Aux.'),('camera-cisco','### VLAN, quyền và luồng video','Vị trí chức năng của bốn camera trên một tầng; vị trí thi công cần khảo sát.')]:
  body=body.replace(marker,f'![{caption}](../latex/assets/{name}.pdf){{width=100%}}\n\n'+marker,1)
 body=body.replace('**','')
 body=re.sub(r'(?m)^.*(?:bản Tiendat|được sửa|đã sửa so với bản|File Packet Tracer gốc của|Các nhãn TV1).*\n','',body)
 body=re.sub(r'!\[[^\]]*\]\(../../02-design/diagrams/exports/physical-(?:main|aux).svg\)\{[^}]*\}\n','',body)
 return body
