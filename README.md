# NewsPortal
Новостной портал созданный на фреймворке django.<br>
Использован Bootstrap v5.3<br>
Реализовано управление постами, Категориями, Комментариями, Авторами через администраторскую панель.<br>
Все формы, возвращают на эту же страницу.<br>
В личном кабинете, лучшая статья стоит первая в списке<br>
Добавлен Shell_requests<br>
Добавлен фильтр цензуры, пока только слово "редиска"<br>
Создание статьи, реализовано через Личный кабинет если пользователь - автор<br>
Редактирование статьи реализовано со страницы просмотра статьи, если на нее зашел её автор<br>
Реализован поиск статьи по автору, типу, категориям и дате<br>
Добавлены модальные окна для авторизации, потверждения удаления статьи и потверждения удаления аккаунта<br>
Добавлена авторизация через Google аккаунт<br>
Добавлена проверка прав доступа на PostCreate и PostEdit<br>
Добавлен переход администратора в админ панель из своего личного кабинета<br>
Редактирование профиля реализовано через вход пользователя в свой профиль<br>
Добавлена массовая рассылка при добавлении новой статьи если они подписаны.<br>
Подписаться на категорию можно нажав на сердечко при просмотре статьи<br>
