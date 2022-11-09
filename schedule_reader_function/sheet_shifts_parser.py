import pandas as pd
from datetime import datetime
import re


class SheetShiftsParser:
    def __is_text_corner(self, val):
        if not val:
            return None
        return re.match("\w+,\s\w+\s\d+", val) != None
        # return

    def __get_corners(self, df):
        corners = []
        for x in range(len(df.columns)):
            for y in range(len(df)):
                if self.__is_text_corner(df.iloc[y][x]):
                    corners.append((x, y))
        return corners

    def __parse_oneday_dataframes(self, df, corners, one_day_shape):
        small_dfs = []
        for corner in corners:
            df = df.copy()
            # small_dfs.append(df.iloc[range(corner[0], corner[0]+one_day_shape[0]), range(corner[1], corner[1]+one_day_shape[1])])
            small_df = df.copy().iloc[
                range(corner[1], min(corner[1] + one_day_shape[1], len(df))),
                range(corner[0], min(corner[0] + one_day_shape[0], len(df.columns))),
            ]
            small_dfs.append(small_df)
        return small_dfs

    def __get_entries(self, small_dataframes):
        entries = []
        for dfs in small_dataframes:
            corner_date = self.__txt_to_date(dfs.iloc[0, 0])
            for y in range(1, len(dfs)):
                first_row_value = dfs.iloc[y, 0]
                if first_row_value:
                    hour_str = first_row_value.split("-")[0]
                    date_and_hour = corner_date.replace(hour=int(hour_str))
                    if dfs.shape[1] >= 3:
                        entries.append([date_and_hour, dfs.iloc[y, 1]])
                        entries.append([date_and_hour, dfs.iloc[y, 2]])
        return entries

    def __txt_to_date(self, txt):
        date_only = datetime.strptime(txt, "%a, %b %d").replace(datetime.now().year)
        return date_only

    def parse(self, flat_data):
        df = pd.DataFrame(flat_data)
        corners = self.__get_corners(df)
        one_day_shape = (corners[2][0] - corners[0][0], corners[1][1] - corners[0][1])
        small_dataframes = self.__parse_oneday_dataframes(df, corners, one_day_shape)
        entries = self.__get_entries(small_dataframes)
        to_send_list = [
            "-".join([dt_tuple[0].strftime("%Y-%m-%d %H:%M"), str(dt_tuple[1])])
            for dt_tuple in entries
            if dt_tuple[1]
        ]
        return to_send_list
