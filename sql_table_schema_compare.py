import pandas as pd

# Assuming df1 and df2 are your two DataFrames containing table schema information

# Define an empty DataFrame to store the differences
differences_df = pd.DataFrame(columns=['Table', 'Column', 'Attribute', 'DF1_Value', 'DF2_Value'])

# Iterate over each table in df1 and compare with df2
for table in df1['Table'].unique():
    # Filter the rows for the current table in both DataFrames
    df1_table = df1[df1['Table'] == table].reset_index(drop=True)
    df2_table = df2[df2['Table'] == table].reset_index(drop=True)
    
    # Iterate over each column in the table
    for column in df1_table['Column']:
        # Check if the column exists in df2_table
        if column not in df2_table['Column'].values:
            differences_df = differences_df.append({'Table': table, 'Column': column,
                                                    'Attribute': 'Column', 'DF1_Value': 'Present', 'DF2_Value': 'Absent'},
                                                   ignore_index=True)
            continue
        
        # Get the data type of the column in both DataFrames
        df1_dtype = df1_table.loc[df1_table['Column'] == column, 'Data Type'].iloc[0]
        df2_dtype = df2_table.loc[df2_table['Column'] == column, 'Data Type'].iloc[0]
        
        # Compare data types
        if df1_dtype != df2_dtype:
            differences_df = differences_df.append({'Table': table, 'Column': column,
                                                    'Attribute': 'Data Type', 'DF1_Value': df1_dtype, 'DF2_Value': df2_dtype},
                                                   ignore_index=True)

# Print the differences DataFrame
print(differences_df)
