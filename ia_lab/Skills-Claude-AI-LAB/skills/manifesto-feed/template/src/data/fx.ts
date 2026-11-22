import {C} from '../lib/theme';
import {K} from './script';
import type {FlashEvent} from '../components/FX';

// Flashes piscantes (duplo pulso + bloom) nas transições por transformação.
// Nenhum flash entre K.incrivelWall + 20 e K.splitLine: o silêncio do paradoxo fica intacto.
export const FLASHES: FlashEvent[] = [
	{at: K.recoil + 2, amp: 0.45},
	{at: K.diveIn + 24, amp: 0.42},
	{at: K.deslizar + 2, amp: 0.16, double: false},
	{at: K.toBelt + 6, amp: 0.36},
	{at: K.perfeito, amp: 0.32, color: C.orange},
	{at: K.contract + 14, amp: 0.42},
	{at: K.lock + 8, amp: 0.55},
	{at: K.produce, amp: 0.28},
	{at: K.produce + 13, amp: 0.12, double: false},
	{at: K.produce + 25, amp: 0.14, double: false},
	{at: K.produce + 36, amp: 0.16, double: false},
	{at: K.produce + 46, amp: 0.2, double: false},
	{at: K.produce + 54, amp: 0.48},
	{at: K.massa, amp: 0.3},
	{at: K.incrivelWall, amp: 0.34},
	{at: K.splitLine, amp: 0.18, double: false},
	{at: K.parar, amp: 0.34, color: C.orange},
	{at: K.suficiente + 44, amp: 0.55},
];
