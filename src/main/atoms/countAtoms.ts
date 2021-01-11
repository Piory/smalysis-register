import { atom } from 'recoil';

const countAtom = atom<number>({
  key: 'countAtom',
  default: 0,
});

export default countAtom;
