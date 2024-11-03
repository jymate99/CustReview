from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
#from wordcloud import WordCloud
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


model=joblib.load(r'best_rf_model_tfidf.joblib')
vectorizer = joblib.load(r'tfidf_vectorizer.joblib')


class TextCleaner(BaseEstimator, TransformerMixin):

    # Transformer to remove punctuation and multiple spaces from text and change uppercase to lowercase

    def __init__(self,pattern="[!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]"):
        self.pattern= pattern
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        X2= X.copy()
        X2.replace({"\s\s+":" "}, regex=False, inplace=True)

        for col in X2.columns:
            if X2.loc[:,col].dtypes == int: continue
            X2.loc[:,col] = X2.loc[:,col].str.replace(self.pattern,"", regex=True).str.lower()
        return X2
    
class StopWordsRemover(BaseEstimator,TransformerMixin):
    # Transformer to remove popular english words with some default exceptions. User can add his own words to keep.
    # This is basically done to ensure keywords remain mostly in the reviews
    def __init__(self,words_to_keep = ['few','all']):
        stop_words = set(stopwords.words('english'))
        self.eng_words = stop_words.difference(set(words_to_keep))

    def fit(self,X,y=None):
        return self

    def transform(self,X):
        X2 = X.copy()

        for col in X2.columns:
            if X2.loc[:, col].dtypes == int:continue
            for en,review in enumerate(X2.loc[:,col].astype(str)):
                new = (" ").join(j for j in review.split(" ") if j.lower() not in self.eng_words)
                try:
                    X2.loc[:,col].iloc[en] = new
                except:
                    continue
            

        return X2

class Stemmer(BaseEstimator,TransformerMixin):
    # Transformer to stem words.
    def __init__(self, stem=True):
        self.stemmer = nltk.PorterStemmer()
        self.stem = stem
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.stem == False:
            return X
        else:
            X2 = X.copy()  
            for col in X2.columns:
                if X2.loc[:, col].dtypes == int: continue
                for en, review in enumerate(X2.loc[:, col].astype(str)):
                    new = (" ").join(self.stemmer.stem(j) for j in review.split(" "))
                    try:
                        X2[:, col].iloc[en] = new
                    except:
                        continue
            return X2
        

preprocessor = Pipeline([
    #at first duplicated reviews will be removed
    #('DuplicateRemover', DuplicatesRemover()),
    #symbols that will be removed are defined in the transformer but a user can define his own/some additional symbols
    #('TextCleaning',TextCleaner()),
    #removing popular english words
    ('StopWordsRemover',StopWordsRemover()),
    #if stem is False the words will not be stemmed
    ('Stemmer', Stemmer()),
    #rating changer, in this example negative(1, 2) ratings are equal to -1, neutral (3) 0 and positive(4,5) 1
    #('Rating', Rating(scale={1:-1, 2:-1, 3:0, 4:1, 5:1})),
    #the autor noticed that after cleaning the reviews some duplicated reviews are left, one more time duplicateremover is used (we could use it only one time, but it would make the process of data cleaning longer)
    #('DuplicateRemover2', DuplicatesRemover())
])

class Text(BaseModel):
    text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost","http://localhost:8000", "http://localhost:80","http://localhost:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TextInput(BaseModel):
    text: str

@app.post("/predict")
async def predict_sentiment(input_data: TextInput):
    # Transform the text using the same vectorizer
    tfidf_vectors_test = vectorizer.transform([input_data.text])
    
    # Make prediction
    prediction = model.predict(tfidf_vectors_test)
    print(prediction[0])
    return {"text": input_data.text, "sentiment": prediction[0]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)