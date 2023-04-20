export const Statistics = ({ verdict, classtype, probability, probabilities }) => {
    if (verdict === "-") {
        return (
            <div>
                <div class="pt-5">
                    class: {classtype}<br></br>
                    probability: {probability} %<br></br>
                    probabilities [accept, decline, suggestion]: {probabilities}<br></br>
                    verdict: {verdict}<br></br>
                    <b>openai does not support statistics</b>
                </div>
            </div>
        )
    }
    return (
        <div class="mt-4 mb-4">
            <div>
                class: {classtype}<br></br>
                probability: {probability} %<br></br>
                probabilities [accept, decline, suggestion]: {probabilities}<br></br>
                verdict: {verdict}<br></br>
            </div>
        </div>
    )
};
