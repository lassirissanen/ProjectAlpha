export const Message = ({message}) => {	

    // the currently logged in user

	function isMessageFromUser() {
        return message.user === "krister";
    }

	return (
		<div class={`${isMessageFromUser() ? "place-self-end" : "place-self-start"} space-y-2`}> 
            <div class={`bg-light-blue text-white p-5 rounded-2xl ${isMessageFromUser() ? "rounded-tr-none" : "rounded-tl-none"}`}>
		        {message.message}
	        </div>
        </div>
	)
}
/**
 * 
 * 	const { user } = null; // the currently logged in user
	function isMessageFromUser() {
        return user?.id === message.user_id;
    }
 */

// ${isMessageFromUser() ? "place-self-end" : "place-self-start"} 

// ${isMessageFromUser() ? "rounded-tr-none" : "rounded-tl-none"}