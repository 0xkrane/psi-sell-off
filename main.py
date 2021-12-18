import json
import pandas as pd
import streamlit as st


@st.cache
def get_psi_sell_data():
    psi_sell_df = pd.read_json(
        'https://api.flipsidecrypto.com/api/v2/queries/843994fd-f982-4a1f-a1da-3ca34f34dcc8/data/latest'
    )
    return psi_sell_df


def main():
    st.title('PSI Sell-off Analysis')

    psi_sell_df = get_psi_sell_data()
    mutated_psi_df = psi_sell_df.copy(deep=True)
    mutated_psi_df['UST_RECEIVED'] = psi_sell_df['FULL_ARR'].apply(
        lambda arr: json.loads(arr)[-1]['amount'] / 10**6
    )
    st.header('Sell-off dataset')
    st.write(mutated_psi_df)

    total_psi_sell_df = mutated_psi_df.groupby('SELLER')[['AMOUNT_SOLD', 'UST_RECEIVED']].sum()
    total_psi_sell_df = total_psi_sell_df.sort_values('AMOUNT_SOLD', ascending=False)
    st.header('Biggest sellers')
    st.write(total_psi_sell_df)

    total_sell_volume = total_psi_sell_df['AMOUNT_SOLD'].sum()
    st.write('Total sell volume (PSI): ', total_sell_volume)

    top_20_sellers = total_psi_sell_df[:20]
    for index, row in top_20_sellers.iterrows():
        st.write('==' * 40)
        st.write(row)
        st.write('https://finder.extraterrestrial.money/mainnet/address/' + index)
        st.write('http://apeboard.finance/dashboard/' + index)
        st.write('https://finder.terra.money/mainnet/address/' + index)


if __name__ == '__main__':
    main()

