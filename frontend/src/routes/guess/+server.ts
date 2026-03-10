import { error, type RequestEvent } from '@sveltejs/kit';
import { coursesMap } from '$lib/domain/server/data-loaders.js';
import { cosineSim, matchWords, scaleCosineSim } from '$lib/domain/sim-calcs';
import type { GuessRequest, GuessResponse } from '$lib/interfaces/guess-server';

export async function POST({ request }: RequestEvent){
	const { guessId, dailyId }: GuessRequest = await request.json();
	const guessCourse = coursesMap.get(guessId);
	const dailyCourse = coursesMap.get(dailyId);

	if (!guessCourse) {
		throw error(400, "Bad guess ID");
	} else if (!dailyCourse) {
		throw error(400, "Bad daily ID");
	}

	const titleFrags = matchWords(guessCourse.title, dailyCourse.title);
    const simScore = scaleCosineSim(cosineSim(guessCourse.vector, dailyCourse.vector));
	const guessResponse: GuessResponse = { titleFrags, simScore }

	return new Response(JSON.stringify(guessResponse));
};