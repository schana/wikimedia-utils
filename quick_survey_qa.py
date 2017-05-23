import pandas as pd

pd.set_option('display.max_columns', 100)
pd.set_option('expand_frame_repr', False)

'''
First, export the data:

mysql --host analytics-store.eqiad.wmnet log -e "select * from QuickSurveysResponses_15266417 where timestamp > 20170515000000 and timestamp < 20170516000000;" > responses.tsv

mysql --host analytics-store.eqiad.wmnet log -e "select * from QuickSurveyInitiation_15278946 where timestamp > 20170515000000 and timestamp < 20170516000000;" > initiation.tsv

Second, download google form responses and name them as <language>_responses.tsv
'''

responses = pd.read_csv('responses.tsv', sep='\t')
initiation = pd.read_csv('initiation.tsv', sep='\t')


def qa_language(language):
    language_initiation = initiation[initiation['wiki'] == '{}wiki'.format(language)]
    impressions = language_initiation[language_initiation['event_eventName'] == 'impression']
    eligible = language_initiation[language_initiation['event_eventName'] == 'eligible']
    language_responses = responses[responses['wiki'] == '{}wiki'.format(language)]
    language_google = pd.read_csv('{}_responses.tsv'.format(language), sep='\t')
    columns = language_google.columns.values
    nice_columns = ['timestamp', 'why_reading', 'prior', 'reading_because', 'event_surveyInstanceToken']
    language_google.columns = nice_columns
    # Limit google forms responses to same time period as the mysql queries
    language_google.index = pd.to_datetime(language_google.pop('timestamp'))
    language_google.index = language_google.index.tz_localize('US/Pacific').tz_convert('UTC')
    language_google = language_google[(language_google.index > pd.to_datetime('2017/05/15 00:00:00')) & (language_google.index < pd.to_datetime('2017/05/16 00:00:00'))]
    print '#' * 80
    print '> wiki'
    print language
    print
    print '> Initiation null values for', language_initiation.shape[0], 'rows'
    print language_initiation.isnull().sum()
    print
    print '> Initiation result type count'
    print language_initiation.groupby('event_eventName').size()
    print
    print '> Initiation unique survey tokens'
    print language_initiation.groupby('event_eventName')['event_surveyInstanceToken'].nunique()
    print
    print '> Responses null values for', language_responses.shape[0], 'rows'
    print language_responses.isnull().sum()
    print
    print '> Responses result type count'
    print language_responses.groupby('event_surveyResponseValue').size()
    print
    print '> Responses unique survey tokens'
    print language_responses.groupby('event_surveyResponseValue')['event_surveyInstanceToken'].nunique()
    print
    print '> Count of impressions with eligible events'
    print pd.merge(impressions, eligible, on='event_surveyInstanceToken')['event_surveyInstanceToken'].nunique()
    print
    print '> Count of responses that do not have a corresponding impression'
    print language_responses[~language_responses['event_surveyInstanceToken'].isin(impressions['event_surveyInstanceToken'])].shape[0]
    print
    print '> Google forms null values for', language_google.shape[0], 'rows'
    print language_google.isnull().sum()
    print
    print '> Registered clicks for google forms'
    count_registered_clicks = language_google.merge(language_responses, on='event_surveyInstanceToken').shape[0]
    print count_registered_clicks
    print
    print '> Registered pageviews for google forms'
    print language_google.merge(eligible, on='event_surveyInstanceToken').shape[0]
    print
    print '> Summary for', language
    print 'Eligible:', eligible.shape[0]
    print 'Impressions:', impressions.shape[0]
    print 'Clicks:', language_responses.shape[0]
    print 'Yes:', language_responses[language_responses['event_surveyResponseValue'] == 'ext-quicksurveys-external-survey-yes-button'].shape[0]
    print 'Google responses:', language_google.shape[0]
    print 'Google responses with registered click:', count_registered_clicks


for language in ('de', 'he', 'ja', 'ro'):
    qa_language(language)

print 'done'


