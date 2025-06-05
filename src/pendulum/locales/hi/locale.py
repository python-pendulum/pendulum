from pendulum.locales.hi.custom import translations as custom_translations


"""
hi locale file.

It has been generated automatically and must not be modified directly.
"""


locale = {
    'plural': lambda n: 'one' if ((n == n and ((n == 0))) or (n == n and ((n == 1)))) else 'other',
    'ordinal': lambda n: 'few' if (n == n and ((n == 4))) else 'many' if (n == n and ((n == 6))) else 'one' if (n == n and ((n == 1))) else 'two' if (n == n and ((n == 2) or (n == 3))) else 'other',
    'translations': {
        'days': {
            'abbreviated': {
                0: 'सोम',
                1: 'मंगल',
                2: 'बुध',
                3: 'गुरु',
                4: 'शुक्र',
                5: 'शनि',
                6: 'रवि',
            },
            'narrow': {
                0: 'सो',
                1: 'मं',
                2: 'बु',
                3: 'गु',
                4: 'शु',
                5: 'श',
                6: 'र',
            },
            'short': {
                0: 'सो',
                1: 'मं',
                2: 'बु',
                3: 'गु',
                4: 'शु',
                5: 'श',
                6: 'र',
            },
            'wide': {
                0: 'सोमवार',
                1: 'मंगलवार',
                2: 'बुधवार',
                3: 'गुरुवार',
                4: 'शुक्रवार',
                5: 'शनिवार',
                6: 'रविवार',
            },
        },
        'months': {
            'abbreviated': {
                1: 'जन॰',
                2: 'फ़र॰',
                3: 'मार्च',
                4: 'अप्रैल',
                5: 'मई',
                6: 'जून',
                7: 'जुल॰',
                8: 'अग॰',
                9: 'सित॰',
                10: 'अक्तू॰',
                11: 'नव॰',
                12: 'दिस॰',
            },
            'narrow': {
                1: 'ज',
                2: 'फ़',
                3: 'मा',
                4: 'अ',
                5: 'म',
                6: 'जू',
                7: 'जु',
                8: 'अ',
                9: 'सि',
                10: 'अ',
                11: 'न',
                12: 'दि',
            },
            'wide': {
                1: 'जनवरी',
                2: 'फ़रवरी',
                3: 'मार्च',
                4: 'अप्रैल',
                5: 'मई',
                6: 'जून',
                7: 'जुलाई',
                8: 'अगस्त',
                9: 'सितंबर',
                10: 'अक्तूबर',
                11: 'नवंबर',
                12: 'दिसंबर',
            },
        },
        'units': {
            'year': {
                'one': '{0} वर्ष',
                'other': '{0} वर्ष',
            },
            'month': {
                'one': '{0} महीना',
                'other': '{0} महीने',
            },
            'week': {
                'one': '{0} सप्ताह',
                'other': '{0} सप्ताह',
            },
            'day': {
                'one': '{0} दिन',
                'other': '{0} दिन',
            },
            'hour': {
                'one': '{0} घंटा',
                'other': '{0} घंटे',
            },
            'minute': {
                'one': '{0} मिनट',
                'other': '{0} मिनट',
            },
            'second': {
                'one': '{0} सेकंड',
                'other': '{0} सेकंड',
            },
            'microsecond': {
                'one': '{0} माइक्रोसेकंड',
                'other': '{0} माइक्रोसेकंड',
            },
        },
        'relative': {
            'year': {
                'future': {
                    'other': '{0} वर्ष में',
                    'one': '{0} वर्ष में',
                },
                'past': {
                    'other': '{0} वर्ष पहले',
                    'one': '{0} वर्ष पहले',
                },
            },
            'month': {
                'future': {
                    'other': '{0} माह में',
                    'one': '{0} माह में',
                },
                'past': {
                    'other': '{0} माह पहले',
                    'one': '{0} माह पहले',
                },
            },
            'week': {
                'future': {
                    'other': '{0} सप्ताह में',
                    'one': '{0} सप्ताह में',
                },
                'past': {
                    'other': '{0} सप्ताह पहले',
                    'one': '{0} सप्ताह पहले',
                },
            },
            'day': {
                'future': {
                    'other': '{0} दिन में',
                    'one': '{0} दिन में',
                },
                'past': {
                    'other': '{0} दिन पहले',
                    'one': '{0} दिन पहले',
                },
            },
            'hour': {
                'future': {
                    'other': '{0} घंटे में',
                    'one': '{0} घंटे में',
                },
                'past': {
                    'other': '{0} घंटे पहले',
                    'one': '{0} घंटे पहले',
                },
            },
            'minute': {
                'future': {
                    'other': '{0} मिनट में',
                    'one': '{0} मिनट में',
                },
                'past': {
                    'other': '{0} मिनट पहले',
                    'one': '{0} मिनट पहले',
                },
            },
            'second': {
                'future': {
                    'other': '{0} सेकंड में',
                    'one': '{0} सेकंड में',
                },
                'past': {
                    'other': '{0} सेकंड पहले',
                    'one': '{0} सेकंड पहले',
                },
            },
        },
        'day_periods': {
            "midnight": "मध्यरात्रि",
            "am": "AM",
            "noon": "दोपहर",
            "pm": "PM",
            "morning1": "सुबह में",
            "afternoon1": "दोपहर में",
            "evening1": "शाम में",
            "night1": "रात में",
        },
        'week_data': {
            'min_days': 1,
            'first_day': 0,
            'weekend_start': 5,
            'weekend_end': 6,
        },
    },
    'custom': custom_translations
}
