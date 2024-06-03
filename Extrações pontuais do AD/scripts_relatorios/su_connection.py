import pymongo


def connection(env, collection='process'):

    if env == 'prod':
        mongo_url = 'mongodb://apiv3:rejceuyf837cku3fck346f97g2i75d3f5fd@mongodb_amazon.portaldolicenciamentosp.com.br:27017/next-producao?readPreference=primary&authSource=admin'
        mongo_env = 'next-producao'

    if env == 'homolog':
        mongo_url = 'mongodb://api-homologv3:u367vcu8c28o6cf2c2f7fc7i27537ki@mongodb_amazon.portaldolicenciamentosp.com.br:27017/next-authorization?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
        mongo_env = 'next-homologacao-sp'

    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_env]
    return db[collection]