const USDollar = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2
});

const formatDecimal = (decimalString) => USDollar.format(decimalString);

export { formatDecimal };
