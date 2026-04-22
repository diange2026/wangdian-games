#!/usr/bin/env python3
"""
工贸企业相关方全流程管理系统 - 演示服务器
启动一个可以直接访问的演示系统
"""

import http.server
import socketserver
import os
import sys
import json
from datetime import datetime
from http import HTTPStatus

# 配置
PORT = 8080
DEMO_DIR = os.path.join(os.path.dirname(__file__), "demo-frontend")
API_MOCK_DATA = {
    "companies": [
        {
            "id": 1,
            "name": "北京建筑安装有限公司",
            "code": "BJ-2024-001",
            "type": "建筑安装",
            "contact_person": "张经理",
            "contact_phone": "13800138001",
            "status": "approved",
            "created_at": "2026-04-22T08:30:00"
        },
        {
            "id": 2,
            "name": "上海机电设备有限公司",
            "code": "SH-2024-002",
            "type": "机电设备",
            "contact_person": "李主任",
            "contact_phone": "13800138002",
            "status": "approved",
            "created_at": "2026-04-22T08:35:00"
        },
        {
            "id": 3,
            "name": "广州安防工程有限公司",
            "code": "GZ-2024-003",
            "type": "安防工程",
            "contact_person": "王工",
            "contact_phone": "13800138003",
            "status": "pending_review",
            "created_at": "2026-04-22T09:10:00"
        }
    ],
    "personnel": [
        {
            "id": 1,
            "personnel_code": "EMP-2024-001",
            "name": "张三",
            "id_card": "110101199001011234",
            "gender": "male",
            "position": "项目经理",
            "work_type": "项目管理",
            "employment_status": "active",
            "status": "approved",
            "company_id": 1,
            "company_name": "北京建筑安装有限公司",
            "created_at": "2026-04-22T08:40:00"
        },
        {
            "id": 2,
            "personnel_code": "EMP-2024-002",
            "name": "李四",
            "id_card": "110101199002021235",
            "gender": "male",
            "position": "安全员",
            "work_type": "安全管理",
            "employment_status": "active",
            "status": "approved",
            "company_id": 1,
            "company_name": "北京建筑安装有限公司",
            "created_at": "2026-04-22T08:45:00"
        },
        {
            "id": 3,
            "personnel_code": "EMP-2024-003",
            "name": "王五",
            "id_card": "110101199003031236",
            "gender": "male",
            "position": "电工",
            "work_type": "电气作业",
            "employment_status": "active",
            "status": "pending_review",
            "company_id": 2,
            "company_name": "上海机电设备有限公司",
            "created_at": "2026-04-22T09:00:00"
        }
    ],
    "certificates": [
        {
            "id": 1,
            "personnel_id": 1,
            "personnel_name": "张三",
            "certificate_type": "特种作业证",
            "certificate_name": "高处作业证",
            "certificate_number": "TSZY-2023-001",
            "issue_date": "2023-01-20",
            "expiry_date": "2026-01-19",
            "certificate_status": "valid",
            "approval_status": "approved",
            "issuing_authority": "市安全生产监督管理局"
        },
        {
            "id": 2,
            "personnel_id": 2,
            "personnel_name": "李四",
            "certificate_type": "特种作业证",
            "certificate_name": "电工作业证",
            "certificate_number": "TSZY-2023-002",
            "issue_date": "2023-03-05",
            "expiry_date": "2026-03-04",
            "certificate_status": "valid",
            "approval_status": "approved",
            "issuing_authority": "市安全生产监督管理局"
        },
        {
            "id": 3,
            "personnel_id": 3,
            "personnel_name": "王五",
            "certificate_type": "特种作业证",
            "certificate_name": "焊工作业证",
            "certificate_number": "TSZY-2023-003",
            "issue_date": "2023-04-10",
            "expiry_date": "2026-04-09",
            "certificate_status": "valid",
            "approval_status": "pending_review",
            "issuing_authority": "市安全生产监督管理局"
        }
    ],
    "stats": {
        "total_companies": 5,
        "active_companies": 3,
        "total_personnel": 10,
        "active_personnel": 8,
        "total_certificates": 15,
        "valid_certificates": 12,
        "expired_certificates": 2,
        "expiring_soon": 3,
        "pending_review": 4
    }
}

class DemoRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义请求处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DEMO_DIR, **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        # API 接口处理
        if self.path.startswith('/api/'):
            self.handle_api_request()
            return
        
        # 静态文件处理
        super().do_GET()
    
    def do_POST(self):
        """处理POST请求"""
        if self.path.startswith('/api/'):
            self.handle_api_post()
            return
        
        self.send_error(HTTPStatus.NOT_FOUND, "File not found")
    
    def handle_api_request(self):
        """处理API请求"""
        try:
            if self.path == '/api/v1/companies/':
                response = {
                    "status": "success",
                    "data": {
                        "items": API_MOCK_DATA["companies"],
                        "total": len(API_MOCK_DATA["companies"]),
                        "page": 1,
                        "page_size": 20,
                        "total_pages": 1
                    },
                    "timestamp": datetime.now().isoformat()
                }
            elif self.path == '/api/v1/personnel/':
                response = {
                    "status": "success",
                    "data": {
                        "items": API_MOCK_DATA["personnel"],
                        "total": len(API_MOCK_DATA["personnel"]),
                        "page": 1,
                        "page_size": 20,
                        "total_pages": 1
                    },
                    "timestamp": datetime.now().isoformat()
                }
            elif self.path == '/api/v1/personnel/1/certificates':
                response = {
                    "status": "success",
                    "data": {
                        "items": [c for c in API_MOCK_DATA["certificates"] if c["personnel_id"] == 1],
                        "total": 1,
                        "page": 1,
                        "page_size": 20,
                        "total_pages": 1
                    },
                    "timestamp": datetime.now().isoformat()
                }
            elif self.path == '/api/v1/stats/':
                response = {
                    "status": "success",
                    "data": API_MOCK_DATA["stats"],
                    "timestamp": datetime.now().isoformat()
                }
            elif self.path == '/api/v1/health':
                response = {
                    "status": "healthy",
                    "service": "工贸企业相关方全流程管理系统",
                    "version": "1.0.0",
                    "timestamp": datetime.now().isoformat(),
                    "uptime": "0 days 0 hours 0 minutes"
                }
            else:
                response = {
                    "status": "error",
                    "message": f"API endpoint {self.path} not found",
                    "timestamp": datetime.now().isoformat()
                }
                self.send_response(HTTPStatus.NOT_FOUND)
            
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
    
    def handle_api_post(self):
        """处理API POST请求"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            
            # 模拟数据创建
            if self.path == '/api/v1/companies/':
                new_id = max(c["id"] for c in API_MOCK_DATA["companies"]) + 1
                new_company = {
                    "id": new_id,
                    "name": post_data.get("name", "新单位"),
                    "code": post_data.get("code", f"NEW-{new_id}"),
                    "type": post_data.get("type", "其他"),
                    "contact_person": post_data.get("contact_person", ""),
                    "contact_phone": post_data.get("contact_phone", ""),
                    "status": "pending_review",
                    "created_at": datetime.now().isoformat()
                }
                API_MOCK_DATA["companies"].append(new_company)
                API_MOCK_DATA["stats"]["total_companies"] += 1
                API_MOCK_DATA["stats"]["pending_review"] += 1
                
                response = {
                    "status": "success",
                    "message": "单位创建成功",
                    "data": new_company,
                    "timestamp": datetime.now().isoformat()
                }
                
            elif self.path == '/api/v1/personnel/':
                new_id = max(p["id"] for p in API_MOCK_DATA["personnel"]) + 1
                new_person = {
                    "id": new_id,
                    "personnel_code": post_data.get("personnel_code", f"EMP-{datetime.now().year}-{new_id:03d}"),
                    "name": post_data.get("name", "新人员"),
                    "id_card": post_data.get("id_card", ""),
                    "gender": post_data.get("gender", "male"),
                    "position": post_data.get("position", ""),
                    "work_type": post_data.get("work_type", ""),
                    "employment_status": "active",
                    "status": "pending_review",
                    "company_id": post_data.get("company_id", 1),
                    "company_name": "新单位",
                    "created_at": datetime.now().isoformat()
                }
                API_MOCK_DATA["personnel"].append(new_person)
                API_MOCK_DATA["stats"]["total_personnel"] += 1
                API_MOCK_DATA["stats"]["pending_review"] += 1
                
                response = {
                    "status": "success",
                    "message": "人员创建成功",
                    "data": new_person,
                    "timestamp": datetime.now().isoformat()
                }
                
            else:
                response = {
                    "status": "error",
                    "message": f"API endpoint {self.path} not found",
                    "timestamp": datetime.now().isoformat()
                }
                self.send_response(HTTPStatus.NOT_FOUND)
            
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
    
    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def main():
    """主函数"""
    print("=" * 60)
    print("🏭 工贸企业相关方全流程管理系统 - 演示服务器")
    print("=" * 60)
    print("")
    print("📁 项目根目录:", os.path.dirname(__file__))
    print("🌐 演示页面目录:", DEMO_DIR)
    print("")
    
    # 确保演示目录存在
    if not os.path.exists(DEMO_DIR):
        os.makedirs(DEMO_DIR)
        print(f"✅ 创建演示目录: {DEMO_DIR}")
    
    # 检查演示文件
    demo_files = os.listdir(DEMO_DIR)
    print(f"📄 演示文件数量: {len(demo_files)}")
    
    try:
        with socketserver.TCPServer(("", PORT), DemoRequestHandler) as httpd:
            print(f"🚀 服务器启动成功!")
            print(f"🌐 访问地址: http://localhost:{PORT}")
            print(f"📚 API文档: http://localhost:{PORT}/api/v1/docs")
            print(f"👤 模拟数据: {len(API_MOCK_DATA['personnel'])} 个人员")
            print(f"🏢 模拟数据: {len(API_MOCK_DATA['companies'])} 个单位")
            print(f"📜 模拟数据: {len(API_MOCK_DATA['certificates'])} 个证书")
            print("")
            print("=" * 60)
            print("🎮 操作指南:")
            print("   1. 在浏览器中打开 http://localhost:8080")
            print("   2. 点击界面上的按钮进行测试")
            print("   3. 使用右上角的搜索框查找数据")
            print("   4. 点击'创建新单位'或'创建新人员'录入数据")
            print("   5. 查看统计报表和预警信息")
            print("=" * 60)
            print("")
            print("📡 服务器运行中... 按 Ctrl+C 停止")
            print("")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 服务器正在停止...")
        print("✅ 演示服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()