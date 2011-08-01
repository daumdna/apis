<?php

function getEvents() {
    global $oauth, $api_url;

    $oauth->fetch($api_url."/calendar/event/index.json");
    $events = json_decode($oauth->getLastResponse());
    
    return $events;
}

function getCategories() {
    global $oauth, $api_url;

    $oauth->fetch($api_url."/calendar/category/index.json");
    $categories = json_decode($oauth->getLastResponse());
    
    return $categories;
}

?>