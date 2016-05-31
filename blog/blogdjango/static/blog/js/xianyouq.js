function hubSpotMessenger(type,message){
	/*type: info, error or success*/
	Messenger.options = {
		extraClasses: 'messenger-fixed messenger-on-bottom messenger-on-right',
		theme: 'future'
	};
	Messenger().post({
		message:message,
		type: type,
		showCloseButton: true
	});
}