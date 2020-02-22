CURR_USD, CURR_EUR = range(1, 3)

CURRENCY_CHOICES = (
    (CURR_USD, 'USD'),
    (CURR_EUR, 'EUR'),
)

SR_PRIVAT, SR_MONO, SR_VKURSE_DP, SR_OBMEN_DP, SR_FINANCE_I_UA = range(1, 6)
SOURCE_CHOICES = (
    (SR_PRIVAT, 'PrivatBank'),
    (SR_MONO, 'MonoBank'),
    (SR_VKURSE_DP, 'vkurse.dp.ua'),
    (SR_OBMEN_DP, 'obmen.dp.ua'),
    (SR_FINANCE_I_UA, 'finance.i.ua'),
)
