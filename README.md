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
Добавлены модельные окна для авторизации, потверждения удаления статьи и потверждения удаления аккаунта<br>
Авторизация работает с любого места на сайте и возвращает туда же<br>
Переписаны View<br>
Код сайта распределен на приложения<br>
