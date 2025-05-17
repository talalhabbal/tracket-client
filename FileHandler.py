import aiofiles
import asyncio
import os

class FileHandler:
    def __init__(self, filename, buffer_size):
        self.filename = filename
        self.buffer = []
        self.buffer_size = buffer_size
        asyncio.create_task(self.write_header())
    
    async def write_header(self):
        if not os.path.exists(self.filename):
            header = "ax,ay,az,gx,gy,gz,recording\n"
            async with aiofiles.open(self.filename, mode='w', newline ='') as file:
                await file.write(header)
                
    async def write_buffer(self):
        if not self.buffer:
            return
        
        async with aiofiles.open(self.filename, mode='a', newline='') as file:
            for row in self.buffer:
                line = ','.join(map(str, row)) + '\n'
                await file.write(line)
                
            self.buffer.clear()
            
    async def add_sample(self, sample):
        self.buffer.append(sample)
        if len(self.buffer) >= self.buffer_size:
            await self.write_buffer()