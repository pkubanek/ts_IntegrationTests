from lsst.ts import salobj

# Create an inherited class from the controller,
# so that you can add logic when commands are received.
# You can also output events and telemetry from there.


class ScriptQueueController(salobj.Controller):
    def __init__(self):
        super().__init__("ScriptQueue", index=2)
        self.cmd_pause.callback = self.do_pause
        self.cmd_add.callback = self.do_add
        self.cmd_resume.callback = self.do_resume

    async def do_pause(self, data):
        # Pause the ScriptQueue to add scripts to the queue.
        # self.log.info("ScriptQueue paused\n")
        pass

    async def do_add(self, data):
        # Add scripts to the ScriptQueue queue.
        # self.log.info("Script: " + data.path)
        # self.log.info("Location: " + data.location)
        pass

    async def do_resume(self, data):
        # Resume the ScriptQueue after adding the scripts
        # to the queue. The ScriptQueue will then execute
        # the scripts.
        # self.log.info("ScriptQueue resumed\n")
        pass

    async def close_tasks(self):
        # This closes the resources for the controller
        await super().close_tasks()

    async def do_move(self):
        pass

    async def do_requeue(self):
        pass

    async def do_showAvailableScripts(self):
        pass

    async def do_showQueue(self):
        pass

    async def do_showSchema(self):
        pass

    async def do_showScript(self):
        pass

    async def do_stopScripts(self):
        pass

    @classmethod
    async def amain(cls) -> None:
        csc = cls()
        print(dir(csc))
        await csc.done_task
