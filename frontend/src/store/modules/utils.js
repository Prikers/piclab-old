const humanReadableSize = (value) => {
  const suffix = 'o';
  const units = ['', 'k', 'M', 'G'];
  let val = parseFloat(value);
  for (let i = 0; i < units.length; i += 1) {
    if (val < 1000.0) {
      return `${val.toFixed(1)} ${units[i]}${suffix}`;
    }
    val /= 1000.0;
  }
  return `${val} 'T'${suffix}`;
};

export default {
  humanReadableSize,
};
