
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from core import VkTools
from data_store import Viewed


'''Отправка сообщений'''


class BotInterface:
    def __init__(self, comunity_token, acces_token):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(acces_token)
        self.params = {}
        self.worksheets = []
        self.offset = 0

    def message_send(self, user_id, message, attachment=None):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'attachment': attachment,
                        'random_id': get_random_id()}
                       )

    def get_photo_string(worksheet['id']):
        photos = self.vk_tools.get_photos(worksheet['id'])
        photo_string = ''
        for photo in photos:
            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'

    '''Получение недостающих данных о пользователе'''

    def get_city(self, event):
        if self.info['city'] is None:
            self.message_send(event.user_id, f'В каком городе ищете пару?')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    self.info['city'] = event.text.capitalize()
                    return self.info['city']

'''Обработка событий / получение сообщений'''

    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    '''Логика для получения данных о пользователе'''
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    self.message_send(
                        event.user_id, f'Привет друг, {self.params["name"]}')
                elif event.text.lower() == 'поиск':
                    '''Логика для поиска анкет'''
                    self.message_send(
                        event.user_id, 'Начинаем поиск')
                    if self.worksheets:
                        worksheet = self.worksheets.pop()
                        get_photo_string(worksheet['id'])
                    else:
                        self.worksheets = self.vk_tools.search_worksheet(
                            self.params, self.offset)

                        worksheet = self.worksheets.pop()

                        '''Проверка анкеты в бд в соответствие с event.user_id'''

                        check_user(engine=engine, profile_id=profile_id,
                                       worksheet_id=worksheet_id)
                        worksheet_id = list.pop()
                        while check_user(worksheet_id):
                            worksheet_id = list.pop()
                        get_photo_string(worksheet['id'])
                        self.offset += 50

                    self.message_send(
                        event.user_id,
                        f'имя: {worksheet["name"]} ссылка: vk.com/{worksheet["id"]}',
                        attachment=photo_string
                    )

                    '''Добавить анкету в бд в соотвествие с event.user_id'''

                    add_user(engine=engine, profile_id=profile_id,
                             worksheet_id=worksheet_id)

                elif event.text.lower() == 'далее':
                    self.message_send(
                        event.user_id, worksheet['id'])

                elif event.text.lower() == 'пока':
                    self.message_send(
                        event.user_id, 'До новых встреч')
                else:
                    self.message_send(
                        event.user_id, 'Неизвестная команда')


