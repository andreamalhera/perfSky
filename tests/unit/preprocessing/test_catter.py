from perfSky.preprocessing.catter import get_task


def test_get_task():
    expected_task = 'CrawlTask'

    assert get_task('CrawlTask(date=2019-09-04_23-23-01, prev_date=2019-09-03_03-44-01)\n') == expected_task
    assert get_task('') == ''
    assert get_task('CrawlTask') == expected_task