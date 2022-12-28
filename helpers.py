
import openai
import pprint as pp
import random


def get_response(prompt):
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
  temperature=0.5,
    max_tokens=200,
    top_p=1.0,
    frequency_penalty=0.52,
    presence_penalty=0.5
)
    answer = response['choices'][0]['text'] 
    
    return answer

def time_method(text: str, say):
    ''' Method to Pass a specific year to GPT3 and get the response
    '''

    #input sanitzation
    if len(text.split()) != 4:
        response = "Please put your request in format: time machine [year] [artists/songs]"
        say(response)
        return
    
    else:
        year = text.split()[2]
        mode = text.split()[3]

    if mode=='artists':
        gpt_input = "Give me 10 musical artists from %s" % year
    elif mode=='songs':
        gpt_input = "Give me 10 songs from %s" % year

    return gpt_input

def genre_method(text: str, say):
    ''' Method to Pass a genre to GPT3 and get the response
    '''

    #input sanitzation
    if len(text.split()) != 3:
        response = "Please put your request in format: genre [genre] [artists/songs]"
        say(response)
        return
    else:
        genre = text.split()[1]
        mode = text.split()[2]

    if mode=='artists':
        gpt_input = "Give me 10 %s artists" % genre
    elif mode=='songs':
        gpt_input = "Give me 10 %s songs" % genre

    return gpt_input

def global_method(text: str, say):
    ''' Method to Pass a country or region to GPT3 and get the response
    '''

    #input sanitzation
    if len(text.split()) != 4:
        response = "Please put your request in format: global explorer [country/region] [artists/songs]"
        say(response)
        return
    else:
        globe = text.split()[2]
        mode = text.split()[3]

    if mode=='artists':
        gpt_input = "Give me 10 artists from %s" % globe
    elif mode=='songs':
        gpt_input = "Give me 10 songs from %s" % globe

    return gpt_input


def popular_method(text: str, say):
    ''' Method to receive back popular music as determined by GPT3
    '''
    if len(text.split()) != 2:
        response = "Please put your request in format single word: popular [artists/songs]"
        say(response)
        return
    else:
        mode = text.split()[1]

    if mode=='artists':
        gpt_input = "Give me 10 random popular artists"
    elif mode=='songs':
        gpt_input = "Give me 10 random popular songs"

    return gpt_input


def surprise_method(text: str, say):
    ''' Method to randomly choose between other options and get the response to gpt3
    '''
    surprise = random.choice(['time','global','popular','genre'])
    mode = random.choice(['artists','songs'])
    
    if surprise=='time':
        possible_years = range(1950,2019) # Playground denotes training really up to 2019
        year = random.choice(possible_years)

        if mode=='artists':
            gpt_input = "Give me 10 musical artists from %s" % year
        elif mode=='songs':
            gpt_input = "Give me 10 songs from %s" % year

        response = 'Giving you a surprise list of %s from the year %s using function time machine' % (mode, year)
        say(response)

    elif surprise=='global':
        regions = ['Africa', 'Asia', 'United States', 'Europe', 'South America', 'England', 'France', 'Pakistan', 'Australia']
        globe = random.choice(regions)

        if mode=='artists':
            gpt_input = "Give me 10 artists from %s" % globe
        elif mode=='songs':
            gpt_input = "Give me 10 songs from %s" % globe

        response = 'Giving you a surprise list of %s from %s using function global explorer' % (mode, globe)
        say(response)

    elif surprise=='genre':
        genres = ['rap','edm','rock','classical','country','randb','metal','jazz']
        genre = random.choice(genres)

        if mode=='artists':
            gpt_input = "Give me 10 %s artists" % genre
        elif mode=='songs':
            gpt_input = "Give me 10 %s songs" % genre

        response = 'Giving you a surprise list of %s from the genre %s using function genre' % (mode, genre)
        say(response)

    elif surprise=='popular':
        if mode=='artists':
            gpt_input = "Give me 10 random popular artists"
        elif mode=='songs':
            gpt_input = "Give me 10 random popular songs"
    
        response = 'Giving you a surprise list of %s using function popular' % (mode)
        say(response)
    
    return gpt_input

def delete_bot_convo_messages(app):
    '''
    Method to clear the bot messages from a conversation, human manually deleted in client 
    as a slack permissions requirement
    '''
    
    # static channel_id of GPTMusic Buddy
    conversation_id = "D010ZJ79U05"

    try:
    # Call the conversations.history method using the WebClient
    # The client passes the token you included in initialization    
        result = app.client.conversations_history(
            channel=conversation_id,
            inclusive=True,
            limit=100
        )

        messages = result['messages']
       
        # Print message text
        print('How many messages to delete: ', len(messages))
        timestamps = [message['ts'] for message in messages]

        for index, timestamp in enumerate(timestamps):
            
            try:
                result = app.client.chat_delete(
                    channel=conversation_id,
                    ts=timestamp
                )
            except:
                print('Not deleting human message: ', messages[index]['text'] )            
    except:
        pass