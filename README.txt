
Connect to "mqtt_server", as "mqtt_client", and subscribe to "mqtt_topic"
When a new value is published, interpret this value as RGB and set the led's to this RGB value

"neopixel_pin" = the pin the neopixel display is connected to
"pixels" = the number of pixels to use (there must be the same number of entries in "leds" as this

config.json
{
	"mqtt_server" : "broker.mqttdashboard.com",
	"mqtt_client" : "clientname",
	"mqtt_topic" : "topic/topic",
	"neopixel_pin" : 14,
	"pixel_count" : 24
}
