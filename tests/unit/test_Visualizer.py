from perfSky import Visualizer as visualizer
import pandas as pd

# TODO: Move this path to a config file
LOG_PATH = './tests/data/input_test_run_point_transformer.csv'

def test_get_relative_timestamps():
    vis = visualizer.Vis()
    df = pd.read_csv(LOG_PATH, index_col=0)
    df = vis.get_relative_timestamps(df, exclude_tasks=[])

    assert set(df.columns).issuperset(['case','activity','rel_start','rel_end','num_start','num_end','start_time','end_time'])