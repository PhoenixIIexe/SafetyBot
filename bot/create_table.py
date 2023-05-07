import data

data.Base.metadata.drop_all(data.engine)
data.Base.metadata.create_all(data.engine)
