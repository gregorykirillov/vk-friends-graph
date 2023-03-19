class VkApiException(BaseException):
    def __init__(self, error_code, error_message):
        self.code = error_code
        self.message = error_message
        super().__init__(f"VK API error {error_code}: {error_message}")
