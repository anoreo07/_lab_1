# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature tăng, phân phối xác suất của các token tiếp theo trở nên "phẳng" hơn, dẫn đến các câu trả lời đa dạng nhưng ít dự đoán được hơn. Ở mức 0.0, mô hình luôn chọn token có xác suất cao nhất (greedy decoding), tạo ra sự nhất quán tuyệt đối; trong khi ở mức 1.5, mô hình bắt đầu chọn các token ít phổ biến hơn, dẫn đến văn phong sáng tạo nhưng dễ gây ra lỗi logic hoặc lặp từ không kiểm soát.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Tôi sẽ đặt temperature ở mức cực thấp, từ 0.0 đến 0.2. Trong hỗ trợ khách hàng, ưu tiên hàng đầu là tính chính xác (factual accuracy) và khả năng tái lập (reproducibility) của câu trả lời; việc sử dụng temperature thấp giúp chatbot bám sát vào cơ sở tri thức (knowledge base) được cung cấp và giảm thiểu tối đa hiện tượng "ảo giác" (hallucination) thông tin.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> GPT-4o đắt hơn chính xác 16.67 lần so với GPT-4o-mini dựa trên đơn giá $0.010/$0.0006. Với tổng lưu lượng 10.5 triệu token một ngày (10k user * 3 lượt * 350 token), chi phí hàng ngày cho GPT-4o là $105, trong khi GPT-4o-mini chỉ là $6.30 — một sự chênh lệch đáng kể có thể ảnh hưởng lớn đến biên lợi nhuận của doanh nghiệp khi quy mô người dùng tăng lên.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> GPT-4o xứng đáng cho các tác vụ đòi hỏi sự tinh tế về ngôn ngữ và tư duy logic cao, chẳng hạn như viết code chuyên sâu, phân tích hợp đồng pháp lý hoặc giải quyết các vấn đề toán học phức tạp nơi sai sót nhỏ có thể gây hậu quả lớn. GPT-4o-mini là lựa chọn tối ưu cho các tác vụ mang tính "thủ tục" như trích xuất thực thể (entity extraction), phân loại email rác, hoặc làm chatbot hỗ trợ các truy vấn đơn giản mà tốc độ phản hồi nhanh và chi phí thấp là yếu tố sống còn.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming là yếu tố then chốt cho trải nghiệm người dùng (UX) trong các ứng dụng chatbot thời gian thực, vì nó giúp tối ưu hóa "Time to First Token" (TTFT), tạo cảm giác phản hồi tức thì và cho phép người dùng bắt đầu xử lý thông tin ngay lập tức thay vì phải chờ đợi toàn bộ khối văn bản lớn được sinh ra. Tuy nhiên, non-streaming lại phù hợp hơn cho các tác vụ xử lý hàng loạt (batch processing), các hệ thống tự động hóa nội bộ nơi kết quả cần được kiểm tra toàn vẹn (ví dụ: xác thực JSON, kiểm tra lỗi cú pháp) trước khi chuyển qua bước tiếp theo, hoặc khi kết nối mạng không ổn định khiến việc duy trì một stream dài gặp rủi ro gián đoạn.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
