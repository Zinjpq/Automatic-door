#include "esp_camera.h"
#include <WiFi.h>
#include "esp_http_server.h"

// Function to start the camera server
void startCameraServer() {
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();

  httpd_uri_t uri = {
    .uri       = "/",
    .method    = HTTP_GET,
    .handler   = [](httpd_req_t *req) {
      camera_fb_t * fb = esp_camera_fb_get();
      if (!fb) {
        httpd_resp_send_500(req);
        return ESP_FAIL;
      }
      httpd_resp_set_type(req, "image/jpeg");
      httpd_resp_send(req, (const char *)fb->buf, fb->len);
      esp_camera_fb_return(fb);
      return ESP_OK;
    },
    .user_ctx  = NULL
  };

  if (httpd_start(&config.server, &config) == ESP_OK) {
    httpd_register_uri_handler(config.server, &uri);
  }
}
