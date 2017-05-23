DATABASE_NAME = 'euc_monitoring'
DATABASE_USER = 'euc_user'
DATABASE_HOST = 'localhost'
DATABASE_PASSWORD = 'fhewwwww~~'
DATABASE_STRING_FORM = "postgresql://{}:{}@{}:5432/{}"
DATABASE_STRING = DATABASE_STRING_FORM.format(DATABASE_USER, DATABASE_PASSWORD,
                                              DATABASE_HOST, DATABASE_NAME)

def getDatabaseString():
    return DATABASE_STRING