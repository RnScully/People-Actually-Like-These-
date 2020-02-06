
import time, sys
from IPython.display import clear_output
import pickle

def update_progress(progress):
    bar_length = 40
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1

    block = int(round(bar_length * progress))

    clear_output(wait = True)
    text = "Progress: [{0}] {1:.1f}%".format( "#" * block + "-" * (bar_length - block), progress * 100)
    print(text)

def save_model(model,name):
    file_ext= '.sav'
    path = 'models/'
    pickle.dump(model, open(path+name+file_ext, 'wb'))

def extract_ngrams(data, num):
    n_grams = ngrams(nltk.word_tokenize(data), num)
    return [ ' '.join(grams) for grams in n_grams]

def vectorizable_ngrams(original_words_list):
    periods = [i.replace('.','. ') for i in original_words_list]
    data =[]
    for rows in periods:
        word_tokens = word_tokenize(rows) 
        data.append(' '.join([w.lower() for w in word_tokens if not w.lower() in my_stop_words]))
    ngram_lst =[extract_ngrams(i,2) for i in data]
    dashngrams = [[grams.replace(' ','-') for grams in ngrams] for ngrams in ngram_lst]
    return dashngrams

def predict_one(string, model_name, vectorizor_name):
    
    path = 'models/'
        
    tfid = pickle.load(open(path+vectorizor_name, 'rb'))
    tfidfed = tfid.transform([string])

    model = pickle.load(open(path+model_name, 'rb'))
    return model.predict(tfidfed)

def predict_many(review_list, model_name, vectorizor_name):
    path = 'models/'
        
    tfid = pickle.load(open(path+vectorizor_name, 'rb'))
    tfidfed = tfid.transform(review_list)

    model = pickle.load(open(path+model_name, 'rb'))
    return model.predict(tfidfed)


# from sklearn.metrics import confusion_matrix
#

def report_score(model, X_test, y_test):
    '''
    a function that reports the accuracy of the model.
    Attributes:
    models (lst): a list of instansiated models to test
    Returns:
    out array, model name, training score, testing score, precision, recall
    '''
    training_score = model.score(X_train, y_train)
    testing_score = model.score(X_test, y_test)
    print('Training score: {}, Testing score: {}'.format(training_score, testing_score))
    tn, fp, fn, tp = confusion_matrix(y_test,model.predict(X_test)).ravel()
    precision = tp/(fp+tp)
    recall = tp/(fn+tp)
    print('tn', '  fp', '  fn', '  tp')
    print(tn, fp, fn, tp)
    print('precision: '+str(precision), 'recall: '+ str(recall))
    out_lst = [training_score, testing_score, precision, recall]
    return out_lst

def remove_parts_of_speech(tokenized_corpus, parts_to_remove):
    '''function which uses nltk position tagging to remove parts of speach
    ++++++++++
    Attributes
    tokenized_corpus (lst): a list of lists: the corpus of documents, each doc transformed into a list of tokens
    parts_to_remove (lst): a list of the NLTK parts of speach that you want removed

    Returns: 
    ++++++++++
    no_pronouns(lst): a list of lists simmilar to tokenized_corpus containing none of the parts of speech you wanted removed
    '''
    remove = set(parts_to_remove)
    no_pronouns = []
    for text in tokenized_corpus:
        j =nltk.pos_tag(text)
        review = []
        for pos in j:
            if pos[1] in remove:
                continue
            else:
                review.append(pos[0])
        no_pronouns.append(review)

    return no_pronouns