from voyager.voyager import Voyager


class QuestLlama(Voyager):
    def __init__(self, azure_login):
        super().__init__(azure_login=azure_login, openai_api_key='not-needed', openai_api_request_timeout=600)

        # system_message = self.action_agent.render_system_message(skills=[])
        # human_message = self.action_agent.render_human_message(
        #     events=self.events, code="", task=self.task, context=context, critique=""
        # )

        # self.action_agent.send_message(system_message)

