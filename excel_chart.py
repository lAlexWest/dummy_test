def generate_data():

    features = ['income', 'age', 'limit']
    data = map(lambda feat: pd.Series(np.random.normal(1000, 1000, (10,))).to_frame(feat).reset_index(), features)
    return list(map(lambda ser: ser.round(2), data))

def write_to_sheet(data, book, sheet, row, col):
    def to_ru_names(col):
        features = ['income', 'age', 'limit']
        translation =['Доход', 'Возраст', 'Лимит']
        mapping = dict(zip(features, translation))
        return mapping.get(col, 'index')
            
    data.rename(columns=to_ru_names, inplace=True)
    
    # Write header
    header = data.columns.to_list()
    sheet.write_row(row, col, header)

    # Write data (column by column)
    for idx, feature_name in enumerate(data):
        sheet.write_column(row+1, col+idx, data[feature_name])

    # Add chart
    bar_chart = book.add_chart({'type': 'column'})
    bar_chart.add_series({
        'values': [sheet.name, row+1, col+1, row+len(data), col+1],
        'categories': [sheet.name, row+1, col, row+len(data), col]
    })
    bar_chart.set_title({'name': data.columns[-1]})
    bar_chart.set_size({'height': len(data)*20})
    sheet.insert_chart(row+1, col+len(data.columns), bar_chart)

    new_row = row + len(data) + 2
    new_col = col
    return new_row, new_col



writer = pd.ExcelWriter('test_file.xlsx')
book = writer.book
cluster_stats_wh = book.add_worksheet('cluster_stats')

row, col = 1, 1
for data in generate_data():
    row, col = write_to_sheet(data, book, cluster_stats_wh, row, col)
writer.close()
