import glob from 'glob';
import { months } from '../utils/constants'

export const getFileNames = (path, raw_date) => {
    const date = new Date(raw_date);
    const pattern = `${date.getFullYear()}_${months[date.getMonth()] || ''}`;
    const options = {cwd: path};
    return glob.sync(`*${pattern}*`, options);
};