export const Message = ({message}) => {	
    
	function isMessageFromUser() {
        return message.user === "customer";
    }

	return (
		<div class={`${isMessageFromUser() ? "place-self-end" : "place-self-start"} space-y-2`}> 
            <div class={`bg-light-blue text-white p-5 rounded-2xl ${isMessageFromUser() ? "rounded-tr-none" : "rounded-tl-none"}`}>
		        {message.message}
	        </div>
        </div>
	)
}