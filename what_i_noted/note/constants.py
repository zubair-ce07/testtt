class NoteAppConstants:
    NOTE_BOOKS_ORDER_BY_HOME_PAGE = ['-is_favorite', '-updated_at']
    NOTE_BOOKS_ORDER_BY_PUBLIC_PAGE = '-updated_at'
    NOTES_ORDER_BY_NOTES_PAGE = ['-is_favorite', '-updated_at']
    NOTES_ORDER_BY_PUBLIC_PAGE = '-updated_at'
    NUMBER_OF_NOTE_BOOKS_ALL_PAGE = 8
    NUMBER_OF_NOTE_BOOKS_HOME_PAGE = 8
    NUMBER_OF_NOTE_BOOKS_PUBLIC_PAGE = 4
    NUMBER_OF_NOTE_LIST_NOTE_PAGE = 8
    NUMBER_OF_NOTE_LIST_PUBLIC_PAGE = 8
    NUMBER_OF_NOTES_ALL_PAGE = 8
    NUMBER_OF_NOTES_PUBLIC_PAGE = 4

    # Messages
    NOTE_BOOK_CREATED = 'New Note Book has been created! You are now able add new Notes to it.'
    NOTE_BOOK_UPDATE_MESSAGE = 'Note Book has been updated!'
    NOTE_CREATED = 'New Note has been added In '
    NOTE_UPDATE_MESSAGE = 'Note  has been updated!'
    SOMETHING_WENT_WRONG = 'Error Something went wrong please try again'
    NO_DATA_FOUND = 'No data found'
    SUCCESS = 'Success!'

    # API's
    GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes?q="
