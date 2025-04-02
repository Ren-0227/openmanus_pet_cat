import sys
import os
import json
import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError
from app.agent.manus import Manus
from app.logger import logger

# 添加项目根目录到 Python 路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# WebSocket 客户端连接集合
connected_clients = set()

async def websocket_handler(websocket, path):
    """
    处理 WebSocket 连接
    - 记录客户端连接
    - 接收并验证消息格式
    - 分发消息到处理逻辑
    """
    client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    connected_clients.add(websocket)
    logger.info(f"客户端已连接: {client_id}")

    try:
        async for message in websocket:
            try:
                # 解析 JSON 消息
                data = json.loads(message)
                if not validate_message(data):
                    await send_to_client(websocket, {"status": "error", "message": "Invalid message format"})
                    continue

                # 根据消息类型分发处理
                if data["type"] == "prompt":
                    await agent_run(websocket, data["data"])
                else:
                    await send_to_client(websocket, {"status": "error", "message": "Unknown message type"})

            except json.JSONDecodeError:
                await send_to_client(websocket, {"status": "error", "message": "Invalid JSON format"})
            except Exception as e:
                logger.error(f"处理消息时发生错误: {str(e)}")
                await send_to_client(websocket, {"status": "error", "message": "Internal server error"})

    except ConnectionClosedError as e:
        logger.info(f"客户端断开连接: {client_id}, 代码: {e.code}, 原因: {e.reason}")
    finally:
        connected_clients.discard(websocket)
        logger.info(f"客户端已移除: {client_id}")

def validate_message(data: dict) -> bool:
    """验证消息格式"""
    return isinstance(data, dict) and "type" in data and "data" in data

async def send_to_client(websocket, message: dict):
    """向单个客户端发送结构化消息"""
    try:
        if websocket.open:
            await websocket.send(json.dumps(message))
    except ConnectionClosedError:
        pass

async def broadcast(message: dict):
    """向所有客户端广播消息"""
    if not connected_clients:
        return

    tasks = []
    for client in connected_clients.copy():
        tasks.append(send_to_client(client, message))
    
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def agent_run(websocket, prompt: str):
    """
    执行 OpenManus 核心逻辑
    - 验证输入
    - 处理耗时操作
    - 实时状态更新
    """
    if not prompt or len(prompt) > 500:
        await send_to_client(websocket, {"status": "error", "message": "Invalid prompt"})
        return

    try:
        # 初始化执行状态
        await send_to_client(websocket, {
            "status": "progress",
            "progress": 0,
            "message": "开始执行..."
        })

        # 执行核心逻辑（示例）
        agent = Manus()
        result = await agent.run(prompt)  # 假设这是耗时操作

        # 发送最终结果
        await send_to_client(websocket, {
            "status": "complete",
            "result": result,
            "message": "执行完成"
        })

    except Exception as e:
        logger.error(f"执行失败: {str(e)}")
        await send_to_client(websocket, {
            "status": "error",
            "message": f"执行错误: {str(e)}"
        })

async def health_check():
    """定时健康检查（可选）"""
    while True:
        await asyncio.sleep(60)
        logger.info(f"当前活跃连接数: {len(connected_clients)}")

async def main():
    """主函数"""
    # 启动健康检查任务
    asyncio.create_task(health_check())

    # 启动 WebSocket 服务器
    async with websockets.serve(
        websocket_handler,
        "localhost",
        8765,
        ping_interval=30,  # 保持连接活跃
        ping_timeout=60
    ):
        logger.info("WebSocket 服务器已在 localhost:8765 启动")
        await asyncio.Future()  # 永久运行

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("服务器已安全关闭")
    except Exception as e:
        logger.error(f"致命错误: {str(e)}")
        sys.exit(1)