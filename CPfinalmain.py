# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 14:06:55 2016

@author: seongyu,hongseok,minhee
"""
from music21 import *
import os
import re
import numpy
from scipy.stats import norm

#악보 받아오기
score = corpus.parse("bach/bwv120.6.mxl")
#악보 제목
title= score.metadata.title
#으뜸음 
key = score.analyze('key').name[0]
#박자
tempo = score.quarterLength

count = dict()

#nameOctaveCount = score.pitchAttributeCount('nameWithOctave')
'''analysis note frequency'''
def countNote(score):
    key = score.analyze('key').name[0]
    count = dict()    
    '''
    for note in score.recurse().getElementsByClass('Note'):
            if not note.name in count:
                count[note.name] = 1
            else:
                count[note.name] += 1
                '''
    count = score.pitchAttributeCount('nameWithOctave')
    convertedCount = convertTone(count,key)
    return convertedCount

def convertTone(count, key):
    conversionValue = {'A':2,'B':1,'C':0,'D':-1,'E':-2,'F':-3,'G':-4}
    convertedCount = dict()
    
    for pitch in count:
        tone = pitch[0]
        octave = pitch[1:]
        
        try :
            if ((ord(tone)) + conversionValue[key]) < 65:
                convertedCount[tone+octave] = count[chr(ord(tone) + conversionValue[key]+7)+octave]
                print(convertedCount[tone+octave])
                #기존 옥타브보다 높은 값으로 가면 값을 낮춰준다.
            elif ((ord(tone)) + conversionValue[key]) > 71:
                convertedCount[tone+octave] = count[chr(ord(tone) + conversionValue[key]-7)+octave]
                print(convertedCount[tone+octave])
            else:
                convertedCount[tone+octave] = count[chr(ord(tone) + conversionValue[key])+octave] 
                print(convertedCount[tone+octave])
        except:
            pass
    return convertedCount       
     
def getSortedKey(count):
    list = []
    for pitch in sorted(count,key=count.get,reverse=True):
        list.append(pitch)
    return list
    
def getSortedValue(count):
    list = []
    for pitch in sorted(count,key=count.get,reverse=True):
        list.append(count[pitch])
    return list
    
'''compareDocumentCorpus'''    
def showComposer():
    composers = ['airdsAirs','bach','beethoven','coconia','corelli','cpebach','demos',
'essenFolkson','handel','haydn','josquin','leadSheet','luca','miscFolk','monteverdi',
'mozart','oneills1850','palestrina','ryansMammoth','schoenberg','schumann','schumann_clara',
'theoryExercises','trecento','verdi','weber']

    for composer in composers:
        print(composer)

    
def getInfoOfScoresByComposer(composer):
    paths = corpus.getComposer(composer)
    
    scoresInfo = []  
    i = 1
    
    for path in paths:
        score = corpus.parse(path)
        tempo = score.quarterLength
        countRate = dict()
        count = score.pitchAttributeCount('nameWithOctave')

        #calculate count ratio, _note count/total count

        for _note in count.keys():
            countRate[_note] = count[_note]/sum(count.values())
            
        _note = getSortedKey(countRate)
        noteRate = getSortedValue(countRate)
        
        scoresInfo.append([score,_note,noteRate,tempo])
        
    return scoresInfo

def compareScoreAndDocument(scoresInfo, documentInfo):
    ss = []
    
    for scoreInfo in scoresInfo:
        notes = scoreInfo[1]
        notesRate = scoreInfo[2]
        words = documentInfo[1]
        wordsRate = documentInfo[2]   
        i = 0
        result = []
        
        #use sum of squares to measure frequency
        if len(notes) > len(words):
            for word in words:
                result.append((notesRate[i]-wordsRate[i])**2)
                i += 1
        else:
            for _note in notes:
                result.append((notesRate[i]-wordsRate[i])**2)
                i += 1
        
        ss.append(sum(result))
        print(sum(result))

    resultIndex = ss.index(min(ss))
    scoreInfo = scoresInfo[resultIndex]
    return scoreInfo

def wordcount(file):

    input_file = open(file,'r')
    worddic = dict()
    empty_str=""
    regex = re.compile('[,\.!?\'\":]')
    from stop_words import get_stop_words
    stop_words = get_stop_words('english')
    stop_words.append('')
    #stopwordlst=['a', 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after', afterwards, again, against, ain’t, all, allow, allows, almost, alone, along, already, also, although, always, am, among, amongst, an, and, another, any, anybody, anyhow, anyone, anything, anyway, anyways, anywhere, apart, appear, appreciate, appropriate, are, aren’t, around, as, aside, ask, asking, associated, at, available, away, awfully, be, became, because, become, becomes, becoming, been, before, beforehand, behind, being, believe, below, beside, besides, best, better, between, beyond, both, brief, but, by, c’mon, c’s, came, can, can’t, cannot, cant, cause, causes, certain, certainly, changes, clearly, co, com, come, comes, concerning, consequently, consider, considering, contain, containing, contains, corresponding, could, couldn’t, course, currently, definitely, described, despite, did, didn’t, different, do, does, doesn’t, doing, don’t, done, down, downwards, during, each, edu, eg, eight, either, else, elsewhere, enough, entirely, especially, et, etc, even, ever, every, everybody, everyone, everything, everywhere, ex, exactly, example, except, far, few, fifth, first, five, followed, following, follows, for, former, formerly, forth, four, from, further, furthermore, get, gets, getting, given, gives, go, goes, going, gone, got, gotten, greetings, had, hadn’t, happens, hardly, has, hasn’t, have, haven’t, having, he, he’s, hello, help, hence, her, here, here’s, hereafter, hereby, herein, hereupon, hers, herself, hi, him, himself, his, hither, hopefully, how, howbeit, however, i’d, i’ll, i’m, i’ve, ie, if, ignored, immediate, in, inasmuch, inc, indeed, indicate, indicated, indicates, inner, insofar, instead, into, inward, is, isn’t, it, it’d, it’ll, it’s, its, itself, just, keep, keeps, kept, know, knows, known, last, lately, later, latter, latterly, least, less, lest, let, let’s, like, liked, likely, little, look, looking, looks, ltd, mainly, many, may, maybe, me, mean, meanwhile, merely, might, more, moreover, most, mostly, much, must, my, myself, name, namely, nd, near, nearly, necessary, need, needs, neither, never, nevertheless, new, next, nine, no, nobody, non, none, noone, nor, normally, not, nothing, novel, now, nowhere, obviously, of, off, often, oh, ok, okay, old, on, once, one, ones, only, onto, or, other, others, otherwise, ought, our, ours, ourselves, out, outside, over, overall, own, particular, particularly, per, perhaps, placed, please, plus, possible, presumably, probably, provides, que, quite, qv, rather, rd, re, really, reasonably, regarding, regardless, regards, relatively, respectively, right, said, same, saw, say, saying, says, second, secondly, see, seeing, seem, seemed, seeming, seems, seen, self, selves, sensible, sent, serious, seriously, seven, several, shall, she, should, shouldn’t, since, six, so, some, somebody, somehow, someone, something, sometime, sometimes, somewhat, somewhere, soon, sorry, specified, specify, specifying, still, sub, such, sup, sure, t’s, take, taken, tell, tends, th, than, thank, thanks, thanx, that, that’s, thats, the, their, theirs, them, themselves, then, thence, there, there’s, thereafter, thereby, therefore, therein, theres, thereupon, these, they, they’d, they’ll, they’re, they’ve, think, third, this, thorough, thoroughly, those, though, three, through, throughout, thru, thus, to, together, too, took, toward, towards, tried, tries, truly, try, trying, twice, two, un, under, unfortunately, unless, unlikely, until, unto, up, upon, us, use, used, useful, uses, using, usually, value, various, very, via, viz, vs, want, wants, was, wasn’t, way, we, we’d, we’ll, we’re, we’ve, welcome, well, went, were, weren’t, what, what’s, whatever, when, whence, whenever, where, where’s, whereafter, whereas, whereby, wherein, whereupon, wherever, whether, which, while, whither, who, who’s, whoever, whole, whom, whose, why, will, willing, wish, with, within, without, won’t, wonder, would, would, wouldn’t, yes, yet, you, you’d, you’ll, you’re, you’ve, your, yours, yourself, yourselves, zero]

    line = input_file.readline()
    while line!= empty_str:
        for word in line.split(' '):
            word=word.rstrip()
            word=regex.sub('',word)
            if not word in stop_words:
                if not word in worddic:
                    worddic[word] = 1 
                else:
                    worddic[word] += 1
        line = input_file.readline()
    
    wordlst=sorted(worddic, key=worddic.__getitem__)
    wordlst.reverse()
    countlst=sorted(worddic.values())
    countlst.reverse()
    
#making freqlst
    freqlst=[]
    for k in countlst:
        freqlst.append(k/sum(countlst)*100)
    
    return wordlst, countlst,freqlst


def getInfoOfDocument(file):
#[name, sortedword,sortedfrequency,tempo,mood]
    documentInfo=[os.path.basename(file),wordcount(file)[0],wordcount(file)[2],textspeed_mood(file)[0],textspeed_mood(file)[1]]

    return documentInfo

# Find the speed of text


# Find the size of the text
def textspeed_mood(file_name):
    while True:
        try:
            bytes = os.path.getsize(file_name)
            #bytes means the size of the file
            break
        
        except os.error:
            print ("Can not find the file or there is an error")
            print ('Please input valid file name')
            file_name = input('Enter file name: ')
            break
    
# Tokenize the words
    texts = open(file_name,'r')
    sentences = [[sentence for sentence in text.lower().split()] for text in texts]
    for sentence in sentences:
        if sentence == []:
            sentences.remove(sentence)
            
# Find the number of . ! ?
    count_end = 0 #Number of end marks
    end_notes = ('?', '!', '.')
    
    for sentence in sentences:
        for word in sentence:
            for end_note in end_notes:
                if end_note in word:
                    count_end = count_end + 1

# sample ratio
    sample_name = ['the_minister_and_the_boy.txt', 'Aladin_and_the_wonderful_lamp.txt', 'alibaba_and_the_40_thieves.txt', 'the_time_machine.txt', 'The_adventure_of_the_empty_house.txt', 'matriarchal_shepherd.txt', 'the_three_little_pigs.txt', 'Obama_nobelprize.txt', 'Alice_Adventures_in_Wonderland.txt', 'The Picture of Dorian Gray.txt', 'THE HOUND OF THE BASKERVILLES.txt', 'A Christmas Carol.txt', 'The Jungle Book.txt', 'The Adventures of Sherlock Holmes.txt.', 'Emma.txt', 'Frankenstein.txt', 'Metamorphosis.txt', 'A Tale of Two Cities.txt', 'War and Peace.txt', 'The Adventures of Tom Sawyer.txt', 'Peter Pan.txt', 'Leviathan.txt', 'Les Misérables.txt', 'The Republic.txt', 'Pygmalion.txt', 'The Wonderful Wizard.txt', 'The Iliad.txt', 'The Prince.txt']
    sample_speed = []
    for file_name in sample_name:
        s_bytes = os.path.getsize(file_name)
        s_texts = open(file_name,'r')
        s_sentences = [[sentence for sentence in text.lower().split()] for text in s_texts]
        for sentence in s_sentences:
            if sentence == []:
                sentences.remove(sentence)
        s_count_end = 0 #Number of end marks
        for sentence in s_sentences:
            for word in sentence:
                for end_note in end_notes:
                    if end_note in word:
                        s_count_end = s_count_end + 1
        sample_speed.append(s_count_end)
                        
    mean = numpy.mean(sample_speed)
    std = numpy.std(sample_speed)
    sample_ratio = [mean,std]    
    
    
# compute the ratio of the size to the number of end marks
    
    speed_ratio = bytes/count_end
    speed_ratio = int(speed_ratio)
    
    Z = (speed_ratio-sample_ratio[0])/sample_ratio[1]
    from scipy.stats import norm
    percent = norm.cdf(Z)
    percent = format(percent,'.2f')
#percent는 상위 몇 퍼센트인지 나타내주는 것 0.xx로 나타남
#percent는 상위 몇 퍼센트인지 나타내주는 것 0.xx로 나타남
    
# Find the mood of text

# Open Good words
    good_words = open('Good.txt','r')
    good_word = [[sentence for sentence in text.lower().split()] for text in good_words]
    for word in good_word:
        if word == []:
            good_word.remove(word)
    
# Open Bad words
    bad_words = open('Bad.txt','r')
    bad_word = [[sentence for sentence in text.lower().split()] for text in bad_words]
    for word in bad_word:
        if word == []:
            bad_word.remove(word)

# Find the number of bad and good words
    count_bad = 0 #Number of bad words
    count_good = 0 #Number of good words
    bad_check = 0
    for sentence in sentences:
        for word in sentence:
            for b_word in bad_word:
                if b_word[0] in word:
                    count_bad = count_bad + 1
                    bad_check = 1
            if bad_check == 0:
                for g_word in good_word:
                    if g_word[0] in word:
                        count_good = count_good + 1
            else:
                bad_check = 0
    ratio = count_bad/count_good

# Sample mood
    sample_name = ['the_minister_and_the_boy.txt', 'Aladin_and_the_wonderful_lamp.txt', 'alibaba_and_the_40_thieves.txt', 'the_time_machine.txt', 'The_adventure_of_the_empty_house.txt', 'matriarchal_shepherd.txt', 'the_three_little_pigs.txt', 'Obama_nobelprize.txt', 'Alice_Adventures_in_Wonderland.txt', 'The Picture of Dorian Gray.txt', 'THE HOUND OF THE BASKERVILLES.txt', 'A Christmas Carol.txt', 'The Jungle Book.txt', 'The Adventures of Sherlock Holmes.txt.', 'Emma.txt', 'Frankenstein.txt', 'Metamorphosis.txt', 'A Tale of Two Cities.txt', 'War and Peace.txt', 'The Adventures of Tom Sawyer.txt', 'Peter Pan.txt', 'Leviathan.txt', 'Les Misérables.txt', 'The Republic.txt', 'Pygmalion.txt', 'The Wonderful Wizard.txt', 'The Iliad.txt', 'The Prince.txt']
    sample_mood = []
    for sample in sample_name:
        count_bad = 0 #Number of bad words
        count_good = 0 #Number of good words
        bad_check = 0
        for sentence in sentences:
            for word in sentence:
                for b_word in bad_word:
                    if b_word[0] in word:
                        count_bad = count_bad + 1
                        bad_check = 1
                if bad_check == 0:
                    for g_word in good_word:
                        if g_word[0] in word:
                            count_good = count_good + 1
                else:
                    bad_check = 0
        ratio = count_bad/count_good
        sample_mood.append(ratio)
        
    mean = numpy.mean(sample_mood)
    std = numpy.std(sample_mood)
    sample_mood = [mean,std]

# Decide the mood of the text
    mood = 0
    R = (ratio - sample_mood[0])/sample_mood[1]
    r = norm.cdf(R)
    if r >= 0.5:
        mood = -1
    else:
        mood = 1
    return percent,mood



#main

#novel import
novel=input(print('Which novel do you want to translate?(including .txt)'))
novelInfo=getInfoOfDocument(novel)

#music import
print('Which composer do you prefer?')
showComposer()
name=input(print('Name of composer:'))
musicInfo=getInfoOfScoresByComposer(name)

compareScoreAndDocument(musicInfo,novelInfo)
