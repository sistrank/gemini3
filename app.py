# image_service.py

from pathlib import Path
import hashlib
import google.generativeai as genai

def generate_use_cases(image_path: str) -> str:
    # Google Generative AI 설정
    genai.configure(api_key="YOUR_API_KEY")

    # 모델 설정
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    # 이미지 업로드 및 해시 생성
    path = Path(image_path)
    hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
    uploaded_file = genai.upload_file(path=path, display_name=hash_id)

    # 프롬프트 생성
    prompt_parts = [
        "이미지의 물건의 다양한 용도를 제시해 줘. 기본적인 용도부터 정말 다양한 용도까지 제시해 줘. 답변은 한글로 주면 감사~",
        uploaded_file,
    ]

    # 생성된 콘텐츠 반환
    response = model.generate_content(prompt_parts)
    return response.text

# 코드 실행 예시
if __name__ == "__main__":
    image_path = "<path>/image0.png"  # 이미지 파일 경로
    use_cases = generate_use_cases(image_path)
    print(use_cases)
