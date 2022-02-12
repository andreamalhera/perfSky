from perfSky.preprocessing.param_cleaner import extract_parameters

def test_extract_parameters():
    test_input = "DumpTask(date=2019-09-04_23-23-01, "\
                 "prev_date=2019-09-03_03-44-01, chunk=prep, "\
                 "sql_filename=review, kvs=(('table_name', "\
                 "u'review_2018_3'),), target_filename=review_2018_3, "\
                 "db_host=db.trustyou.com, db_port=5432, db_user=daily, "\
                 "db_name=ty_analytic)"
    expected_output = {
            'date': '2019-09-04_23-23-01',
            'prev_date': '2019-09-03_03-44-01',
            'chunk': 'prep',
            'sql_filename': 'review',
            'kvs': "(('table_name', u'review_2018_3'),)",
            'target_filename': 'review_2018_3',
            'db_host': 'db.trustyou.com',
            'db_port': '5432',
            'db_user': 'daily',
            'db_name': 'ty_analytic'
            }
    assert extract_parameters(test_input) == expected_output
    assert extract_parameters('CrawlTask') is None
