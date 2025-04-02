import asyncio
import websockets
from app.agent.manus import Manus
from app.logger import logger

# WebSocket客户端连接集合
connected_clients = set()

# 处理WebSocket连接
async def websocket_handler(websocket, path):
    connected_clients.add(websocket)
    logger.info(f"客户端已连接: {websocket.remote_address}")
    try:
        async for message in websocket:
            logger.info(f"收到消息: {message}")
            await send_to_frontend("开始执行...")
            await agent_run(message)
    except websockets.exceptions.ConnectionClosedOK:
        logger.info("客户端正常断开连接")
    except Exception as e:
        logger.error(f"连接处理失败: {e}")
    finally:
        connected_clients.discard(websocket)
        logger.info(f"客户端已断开连接: {websocket.remote_address}")

# 发送消息到所有连接的前端客户端
async def send_to_frontend(message):
    if connected_clients:
        tasks = []
        for client in connected_clients.copy():
            if client.open:
                tasks.append(client.send(message))
            else:
                connected_clients.discard(client)
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

# 模拟 agent.run 的函数
async def agent_run(prompt):
    logger.info(f"Executing prompt: {prompt}")
    await send_to_frontend(f"正在执行: {prompt}")
    await asyncio.sleep(1)  # 模拟处理时间
    logger.info("Request processed.")
    await send_to_frontend("执行完成")

# 主函数
async def main():
    global agent
    agent = Manus()
    async with websockets.serve(websocket_handler, "localhost", 8765):
        logger.info("WebSocket服务器已启动，等待前端连接...")
        await asyncio.Future()  # 运行事件循环

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"发生错误: {e}")