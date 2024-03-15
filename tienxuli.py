import re
import numpy as np
from pyvi import ViTokenizer

def remove_icon(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           "]+", flags=re.UNICODE)
    text_without_emoji = emoji_pattern.sub(r'', text)
    
    non_alphanumeric_pattern = r'[^\w\s]'
    text_without_non_alphanumeric = re.sub(non_alphanumeric_pattern, "", text_without_emoji)
    
    return text_without_non_alphanumeric

# Danh sách từ viết tắt và từ thay thế
abbreviations = {
    'ctrai': 'con trai',
    'khôg': 'không',
    'bme': 'bố mẹ',
    'cta': 'chúng ta',
    'mih': 'mình',
    'mqh': 'mối quan hệ',
    'cgai': 'con gái',
    'nhữg': 'những',
    'mng': 'mọi người',
    'svtn': 'sinh viên tình nguyện',
    'r': 'rồi',
    'qtam': 'quan tâm',
    'thươg': 'thương',
    'qtâm': 'quan tâm',
    'chug': 'chung',
    'trườg': 'trường',
    'thoy': 'thôi',
    'đki': 'đăng ký',
    'atsm': 'ảo tưởng sức mạnh',
    'ạk': 'ạ',
    'cv': 'công việc',
    'vch': 'vãi chưởng',
    'cùg': 'cùng',
    'pn': 'bạn',
    'pjt': 'biết',
    'thjk': 'thích',
    'keke': 'ce ce',
    'ktra': 'kiểm tra',
    'nek': 'nè',
    'cgái': 'con gái',
    'nthe': 'như thế',
    'chúg': 'chúng',
    'kái': 'cái',
    'tìh': 'tình',
    'phòg': 'phòng',
    'lòg': 'lòng',
    'từg': 'từng',
    'rằg': 'rằng',
    'sốg': 'sống',
    'thuj': 'thôi',
    'thuơng': 'thương',
    'càg': 'càng',
    'đky': 'đăng ký',
    'bằg': 'bằng',
    'sviên': 'sinh viên',
    'ák': 'á',
    'đág': 'đáng',
    'nvay': 'như vậy',
    'nhjeu': 'nhiều',
    'xg': 'xuống',
    'zồi': 'rồi',
    'trag': 'trang',
    'zữ': 'dữ',
    'atrai': 'anh trai',
    'kte': 'kinh tế',
    'độg': 'động',
    'lmht': 'liên minh huyền thoại',
    'gắg': 'gắng',
    'đzai': 'đẹp trai',
    'thgian': 'thời gian',
    'plz': 'pờ ly',
    'đồg': 'đồng',
    'btrai': 'bạn trai',
    'nthê': 'như thế',
    'hìhì': 'hì hì',
    'vọg': 'vọng',
    'hihe': 'hi he',
    'đôg': 'đông',
    'răg': 'răng',
    'thườg': 'thường',
    'tcảm': 'tình cảm',
    'đứg': 'đứng',
    'ksao': 'không sao',
    'dz': 'đẹp trai',
    'hjxhjx': 'hix hix',
    'cmày': 'chúng mày',
    'xuốg': 'xuống',
    'nkư': 'như',
    'lquan': 'liên quan',
    'tiếg': 'tiếng',
    'hajz': 'hai',
    'xih': 'xinh',
    'hìh': 'hình',
    'thàh': 'thành',
    'ngke': 'nghe',
    'dzậy': 'dậy',
    'teencode': 'tin cốt',
    'tnào': 'thế nào',
    'tưởg': 'tưởng',
    'ctrinh': 'chương trình',
    'phog': 'phong',
    'hôg': 'không',
    'zìa': 'gì',
    'kũg': 'cũng',
    'ntnao': 'như thế nào',
    'trọg': 'trọng',
    'nthế': 'như thế',
    'năg': 'năng',
    'ngđó': 'người đó',
    'lquen': 'làm quen',
    'riêg': 'riêng',
    'ngag': 'ngang',
    'hêhê': 'hê hê',
    'bnhiu': 'bao nhiêu',
    'ngốk': 'ngốc',
    'kậu': 'cậu',
    'highland': 'hai lừn',
    'kqua': 'kết quả',
    'htrc': 'hôm trước',
    'địh': 'định',
    'gđình': 'gia đinh',
    'giốg': 'giống',
    'csống': 'cuộc sống',
    'xug': 'xùng',
    'zùi': 'rồi',
    'bnhiêu': 'bao nhiêu',
    'cbị': 'chuẩn bị',
    'kòn': 'còn',
    'buôg': 'buông',
    'csong': 'cuộc sống',
    'chàg': 'chàng',
    'chăg': 'chăng',
    'ngàh': 'ngành',
    'llac': 'liên lạc',
    'nkưng': 'nhưng',
    'nắg': 'nắng',
    'tíh': 'tính',
    'khoảg': 'khoảng',
    'thík': 'thích',
    'ngđo': 'người đó',
    'ngkhác': 'người khác',
    'thẳg': 'thẳng',
    'kảm': 'cảm',
    'dàh': 'dành',
    'júp': 'giúp',
    'lặg': 'lặng',
    'vđê': 'vấn đề',
    'bbè': 'bạn bè',
    'bóg': 'bóng',
    'dky': 'đăng ký',
    'dòg': 'dòng',
    'uốg': 'uống',
    'tyêu': 'tình yêu',
    'snvv': 'sinh nhật vui vẻ',
    'đthoại': 'điện thoại',
    'qhe': 'quan hệ',
    'cviec': 'công việc',
    'tượg': 'tượng',
    'qà': 'quà',
    'thjc': 'thích',
    'nhưq': 'nhưng',
    'cđời': 'cuộc đời',
    'bthường': 'bình thường',
    'zà': 'già',
    'đáh': 'đánh',
    'xloi': 'xin lỗi',
    'zám': 'dám',
    'qtrọng': 'quan trọng',
    'bìh': 'bình',
    'lzi': 'làm gì',
    'qhệ': 'quan hệ',
    'đhbkhn': 'đại học bách khoa hà nội',
    'hajzz': 'hai',
    'kủa': 'của',
    'lz': 'làm gì',
    'đhkhtn': 'đại học khoa học tự nhiên',
    'đóg': 'đóng',
    'cka': 'cha',
    'lgi': 'làm gì',
    'nvậy': 'như vậy',
    'qả': 'quả',
    'đkiện': 'điều kiện',
    'nèk': 'nè',
    'tlai': 'tương lai',
    'bsĩ': 'bác sĩ',
    'hkì': 'học kỳ',
    'đcsvn': 'đảng cộng sản việt nam',
    'vde': 'vấn đề',
    'chta': 'chúng ta',
    'òy': 'rồi',
    'ltinh': 'linh tinh',
    'ngyeu': 'người yêu',
    'đthoai': 'điện thoại',
    'snghĩ': 'suy nghĩ',
    'nặg': 'nặng',
    'họk': 'học',
    'dừg': 'dừng',
    'hphúc': 'hạnh phúc',
    'hiha': 'hi ha',
    'wtâm': 'quan tâm',
    'thíck': 'thích',
    'chuện': 'chuyện',
    'lạh': 'lạnh',
    'fây': 'phây',
    'ntnày': 'như thế này',
    'lúk': 'lúc',
    'haj': 'hai',
    'ngía': 'nghía',
    'mớj': 'mới',
    'hsơ': 'hồ sơ',
    'ctraj': 'con trai',
    'nyêu': 'người yêu',
    'điiiiiii': 'đi',
    'rồii': 'rồi',
    'c': 'chị',
    'kih': 'kinh',
    'kb': 'kết bạn',
    'hixxx': 'hích',
    'dthương': 'dễ thương',
    'nhiềuuu': 'nhiều',
    'ctrình': 'chương trình',
    'mìnk': 'mình',
    'mjh': 'mình',
    'ng': 'người',
    'vc': 'vợ chồng',
    'uhm': 'ừm',
    'thỳ': 'thì',
    'nyc': 'người yêu cũ',
    'tks': 'thanks',
    'nàg': 'nàng',
    'thôii': 'thôi',
    'đjên': 'điên',
    'bgái': 'bạn gái',
    'vớii': 'với',
    'xink': 'xinh',
    'hđộng': 'hành động',
    'đhọc': 'đại học',
    'mk': 'mình',
    'bn': 'bạn',
    'thik': 'thích',
    'cj': 'chị',
    'mn': 'mọi người',
    'nguoi': 'người',
    'nógn': 'nóng',
    'hok': 'không',
    'ko': 'không',
    'bik': 'biết',
    'vs': 'với',
    'cx': 'cũng',
    'mik': 'mình',
    'wtf': 'what the fuck',
    'đc': 'được',
    'cmt': 'comment',
    'ck': 'chồng',
    'chk': 'chồng',
    'ngta': 'người ta',
    'gđ': 'gia đình',
    'oh': 'ồ',
    'vk': 'vợ',
    'ctác': 'công tác',
    'sg': 'sài gòn',
    'ae': 'anh em',
    'ah': 'à',
    'ạh': 'ạ',
    'rì': 'gì',
    'ms': 'mới',
    'vn': 'việt nam',
    'nhaa': 'nha',
    'cũg': 'cũng',
    'đag': 'đang',
    'ơiii': 'ơi',
    'hic': 'hích',
    'ace': 'anh chị em',
    'àk': 'à',
    'uh': 'ừ',
    'cmm': 'con mẹ mày',
    'cmnr': 'con mẹ nó rồi',
    'ơiiii': 'ơi',
    'hnay': 'hôm nay',
    'ukm': 'ừm',
    'tq': 'trung quốc',
    'ctr': 'chương trình',
    'đii': 'đi',
    'nch': 'nói chuyện',
    'trieu': 'triệu',
    'hahah': 'ha ha',
    'nta': 'người ta',
    'ngèo': 'nghèo',
    'kêh': 'kênh',
    'ak': 'à',
    'ad': 'admin',
    'j': 'gì',
    'ny': 'người yêu',
    'dc': 'được',
    'qc': 'quảng cáo',
    'baoh': 'bao giờ',
    'zui': 'vui',
    'zẻ': 'vẻ',
    'tym': 'tim',
    'aye': 'anh yêu em',
    'eya': 'em yêu anh',
    'fb': 'facebook',
    'insta': 'instagram',
    'z': 'vậy',
    'thich': 'thích',
    'vcl': 'vờ cờ lờ',
    'đt': 'điện thoại',
    'acc': 'account',
    'lol': 'lồn',
    'loz': 'lồn',
    'lozz': 'lồn',
    'trc': 'trước',
    'chs': 'chẳng hiểu sao',
    'đhs': 'đéo hiểu sao',
    'qá': 'quá',
    'ntn': 'như thế nào',
    'wá': 'quá',
    'zậy': 'vậy',
    'zô': 'vô',
    'ytb': 'youtube',
    'vđ': 'vãi đái',
    'vchg': 'vãi chưởng',
    'sml': 'sấp mặt lờ',
    'xl': 'xin lỗi',
    'cmn': 'con mẹ nó',
    'face': 'facebook',
    'hjhj': 'hi hi',
    'vv': 'vui vẻ',
    'ns': 'nói',
    'iu': 'yêu',
    'vcđ': 'vãi cải đái',
    'in4': 'info',
    'qq': 'quằn què',
    'sub': 'subcribe',
    'kh': 'không',
    'zạ': 'vậy',
    'oy': 'rồi',
    'jo': 'giờ',
    'clmm': 'cái lồn mẹ mày',
    'bsvv': 'buổi sáng vui vẻ',
    'troai': 'trai',
    'wa': 'quá',
    'hjx': 'hix',
    'e': 'em',
    'ik': 'ý',
    'ji': 'gì',
    'ce': 'chị em',
    'lm': 'làm',
    'đz': 'đẹp giai',
    'sr': 'sorry',
    'ib': 'inbox',
    'hoy': 'thôi',
    'đbh': 'đéo bao giờ',
    'k': 'không',
    'vd': 'ví dụ',
    'a': 'anh',
    'cũng z': 'cũng vậy',
    'z là': 'vậy là',
    'unf': 'unfriend',
    'my fen': 'my friend',
    'fen': 'friend',
    'cty': 'công ty',
    'on lai': 'online',
    'u hai ba': 'u23',
    'kô': 'không',
    'đtqg': 'đội tuyển quốc gia',
    'hqua': 'hôm qua',
    'xog': 'xong',
    'uh': 'ừ',
    'uk': 'ừ',
    'nhoé': 'nhé',
    'biet': 'biết',
    'quí': 'quý',
    'stk': 'số tài khoản',
    'hong kong': 'hồng kông',
    'đươc': 'được',
    'nghành': 'ngành',
    'nvqs': 'nghĩa vụ quân sự',
    'ngừoi': 'người',
    'trog': 'trong',
    'tgian': 'thời gian',
    'biêt': 'biết',
    'fải': 'phải',
    'nguời': 'người',
    'tđn': 'thế đéo nào',
    'bth': 'bình thường',
    'vcđ': 'vãi cả đái',
    'tgdd': 'thế giới di động',
    'khg': 'không',
    'nhưg': 'nhưng',
    'thpt': 'trung học phổ thông',
    'thằg': 'thằng',
    'đuợc': 'được',
    'dc': 'được',
    'đc': 'được',
    'ah': 'à',
    'àh': 'à',
    'ku': 'cu',
    'thým': 'thím',
    'onl': 'online',
    'zô': 'dô',
    'zú': 'vú',
    'cmnd': 'chứng minh nhân dân',
    'sđt': 'số điện thoại',
    'klq': 'không liên quan'
}
english = {'you': 'bạn', 'cute': 'dễ thương', 'funny': 'hài hước', 'fun': 'vui', 'sad': 'buồn bã', 'cool': 'ngầu', 'kool': 'ngầu', 'love': 'yêu', 'like': 'thích', 'hate': 'ghét', 'awesome': 'tuyệt vời', 'amazing': 'tuyệt vời', 'beautiful': 'đẹp đẽ', 'ugly': 'xấu xí', 'happy': 'hạnh phúc', 'excited': 'hào hứng', 'tired': 'mệt mỏi', 'lazy': 'lười biếng', 'smart': 'thông minh', 'stupid': 'ngu ngốc', 'best': 'tốt nhất', 'worst': 'tệ nhất', 'hot': 'nóng hổi', 'cold': 'lạnh lùng', 'crazy': 'điên đảo', 'normal': 'bình thường', 'weird': 'kỳ cục', 'fantastic': 'tuyệt vời', 'fabulous': 'tuyệt vời', 'awkward': 'ngượng ngùng', 'brave': 'dũng cảm', 'scared': 'sợ hãi', 'strange': 'lạ lùng', 'sweet': 'ngọt ngào', 'silly': 'ngốc nghếch', 'strong': 'mạnh mẽ', 'weak': 'yếu đuối', 'true': 'đúng', 'false': 'sai', 'honest': 'trung thực', 'dishonest': 'không trung thực', 'stressed': ' căng thẳng', 'relaxed': 'thư giãn', 'busy': 'bận rộn', 'free': 'trống rỗng', 'serious': 'nghiêm túc', 'friendly': 'thân thiện', 'unfriendly': 'không thân thiện', 'polite': 'lịch sự', 'rude': 'thô lỗ', 'surprised': 'ngạc nhiên', 'bored': 'chán chường', 'creative': 'sáng tạo', 'boring': 'buồn chán', 'interesting': 'thú vị', 'simple': 'đơn giản', 'complicated': 'phức tạp', 'modern': 'hiện đại', 'traditional': 'truyền thống', 'popular': 'phổ biến', 'unpopular': 'không phổ biến', 'old': 'cũ kỹ', 'new': 'mới mẻ', 'old-fashioned': 'lạc hậu', 'trendy': 'thời trang', 'outdated': 'lạc hậu', 'rich': 'giàu có', 'poor': 'nghèo đói', 'successful': 'thành công', 'unsuccessful': 'không thành công', 'safe': 'an toàn', 'dangerous': 'nguy hiểm', 'clean': 'sạch sẽ', 'dirty': 'bẩn thỉu', 'easy': 'dễ dàng', 'difficult': 'khó khăn', 'delicious': 'ngon miệng', 'disgusting': 'ghê tởm', 'lucky': 'may mắn', 'unlucky': 'đen đủi', 'sour': 'chua chát', 'tall': 'cao lớn', 'short': 'ngắn ngủn', 'thick': 'dày dặn', 'thin': 'mảnh mai', 'fast': 'nhanh chóng', 'slow': 'chậm rãi', 'loud': 'ồn ào', 'quiet': 'yên tĩnh', 'bright': 'sáng sủa', 'dark': 'tối tăm', 'expensive': 'đắt đỏ', 'cheap': 'rẻ tiền', 'good': 'tốt', 'bad': 'xấu xa', 'big': 'to lớn', 'small': 'nhỏ bé', 'empty': 'trống rỗng', 'full': 'đầy ắp', 'early': 'sớm sửa', 'late': 'muộn màng'}
sentiment_words = {'ô kêi': 'ok', 'okie': 'ok', 'o kê': 'ok', 'okey': 'ok', 'ôkê': 'ok', 'oki': 'ok', 'oke': 'ok', 'okay': 'ok', 'okê': 'ok', 'kô': 'không', 'kp': 'không phải', 'ko': 'không', 'khong': 'không', 'hok': 'không', 'wa': 'quá', 'wá': 'quá', 'authentic': 'chính hãng', 'auth': 'chính hãng', 'gud': 'tốt', 'wel done': 'tốt', 'well done': 'tốt', 'good': 'tốt', 'gút': 'tốt', 'sấu': 'xấu', 'gut': 'tốt', 'tot': 'tốt', 'nice': 'tốt', 'perfect': 'rất tốt', 'qá': 'quá', 'mik': 'mình', 'product': 'sản phẩm', 'quality': 'chất lượng', 'excelent': 'tuyệt vời', 'excellent': 'tuyệt vời', 'bad': 'tệ', 'fresh': 'tươi', 'sad': 'buồn', 'quickly': 'nhanh', 'quick': 'nhanh', 'fast': 'nhanh', 'beautiful': 'đẹp', 'chất lg': 'chất lượng', 'sài': 'xài', 'thik': 'thích', 'very': 'rất', 'dep': 'đẹp', 'xau': 'xấu', 'delicious': 'ngon', 'hàg': 'hàng', 'iu': 'yêu', 'fake': 'giả mạo', 'poor': 'tệ', 'pro': 'chuyên nghiệp', 'cons': 'nhược điểm', 'khuyến mãi': 'ưu đãi', 'sale': 'giảm giá', 'discount': 'giảm giá', 'km': 'ưu đãi', 'advantage': 'ưu điểm', 'disadvantage': 'nhược điểm', 'happy': 'hạnh phúc', 'unhappy': 'không hạnh phúc', 'happiness': 'hạnh phúc', 'love': 'yêu thương', 'like': 'thích', 'dislike': 'không thích', 'hate': 'ghét', 'awesome': 'tuyệt vời', 'amazing': 'tuyệt vời', 'cool': 'ngầu', 'ugly': 'xấu xí', 'fun': 'vui', 'boring': 'buồn chán', 'exciting': 'hứng thú', 'interesting': 'thú vị', 'creative': 'sáng tạo', 'ordinary': 'bình thường', 'unique': 'duy nhất', 'common': 'phổ biến', 'rare': 'hiếm', 'delightful': 'dễ chịu', 'displeasing': 'không dễ chịu', 'satisfactory': 'đạt yêu cầu', 'unsatisfactory': 'không đạt yêu cầu', 'acceptable': 'chấp nhận được', 'unacceptable': 'không chấp nhận được', 'agree': 'đồng ý', 'disagree': 'không đồng ý', 'succeed': 'thành công', 'fail': 'thất bại', 'support': 'ủng hộ', 'oppose': 'phản đối', 'trust': 'tin tưởng', 'distrust': 'nghi ngờ', 'improve': 'cải thiện', 'worsen': 'xấu đi', 'helpful': 'hữu ích', 'unhelpful': 'không hữu ích', 'polite': 'lịch sự', 'impolite': 'thô lỗ', 'fortunate': 'may mắn', 'unfortunate': 'đen đủi', 'praise': 'khen ngợi', 'criticize': 'phê phán', 'recommend': 'khuyến khích', 'discourage': 'nản lòng', 'congratulate': 'chúc mừng', 'condolences': 'động viên', 'victory': 'chiến thắng', 'defeat': 'thất bại', 'peace': 'hòa bình', 'conflict': 'xung đột', 'success': 'thành công', 'failure': 'thất bại', 'wealth': 'giàu có', 'poverty': 'nghèo đói', 'luxury': 'xa xỉ', 'simplicity': 'đơn giản', 'generous': 'rộng lượng', 'selfish': 'ích kỷ', 'brave': 'dũng cảm', 'coward': 'nhát gan', 'proud': 'tự hào', 'shameful': 'đáng xấu hổ', 'loyal': 'trung thành', 'betray': 'phản bội', 'forgive': 'tha thứ', 'vengeance': 'trả thù', 'forgiving': 'tha thứ', 'unforgiving': 'không tha thứ'}


def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic
dicchar = loaddicchar()
# Hàm chuyển Unicode dựng sẵn về Unicde tổ hợp (phổ biến hơn)
def convert_unicode(txt):
    return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)


bang_nguyen_am = [['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
                  ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
                  ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
                  ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e'],
                  ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
                  ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i'],
                  ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o'],
                  ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'oo'],
                  ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
                  ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u'],
                  ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
                  ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y']]
bang_ky_tu_dau = ['', 'f', 's', 'r', 'x', 'j']


nguyen_am_to_ids = {}

for i in range(len(bang_nguyen_am)):
    for j in range(len(bang_nguyen_am[i]) - 1):
        nguyen_am_to_ids[bang_nguyen_am[i][j]] = (i, j)

def chuan_hoa_dau_tu_tieng_viet(word):
    if not is_valid_vietnam_word(word):
        return word

    chars = list(word)
    dau_cau = 0
    nguyen_am_index = []
    qu_or_gi = False
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        elif x == 9:  # check qu
            if index != 0 and chars[index - 1] == 'q':
                chars[index] = 'u'
                qu_or_gi = True
        elif x == 5:  # check gi
            if index != 0 and chars[index - 1] == 'g':
                chars[index] = 'i'
                qu_or_gi = True
        if y != 0:
            dau_cau = y
            chars[index] = bang_nguyen_am[x][0]
        if not qu_or_gi or index != 1:
            nguyen_am_index.append(index)
    if len(nguyen_am_index) < 2:
        if qu_or_gi:
            if len(chars) == 2:
                x, y = nguyen_am_to_ids.get(chars[1])
                chars[1] = bang_nguyen_am[x][dau_cau]
            else:
                x, y = nguyen_am_to_ids.get(chars[2], (-1, -1))
                if x != -1:
                    chars[2] = bang_nguyen_am[x][dau_cau]
                else:
                    chars[1] = bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else bang_nguyen_am[9][dau_cau]
            return ''.join(chars)
        return word

    for index in nguyen_am_index:
        x, y = nguyen_am_to_ids[chars[index]]
        if x == 4 or x == 8:  # ê, ơ
            chars[index] = bang_nguyen_am[x][dau_cau]
            return ''.join(chars)

    if len(nguyen_am_index) == 2:
        if nguyen_am_index[-1] == len(chars) - 1:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
        else:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    else:
        x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
        chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    return ''.join(chars)


def is_valid_vietnam_word(word):
    chars = list(word)
    nguyen_am_index = -1
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x != -1:
            if nguyen_am_index == -1:
                nguyen_am_index = index
            else:
                if index - nguyen_am_index != 1:
                    return False
                nguyen_am_index = index
    return True


def chuan_hoa_dau_cau_tieng_viet(sentence):
    sentence = sentence.lower()
    words = sentence.split()
    for index, word in enumerate(words):
        cw = re.sub(r'(^\\p{P}*)([p{L}.]*\\p{L}+)(\\p{P}*$)', r'\1/\2/\3', word).split('/')
        if len(cw) == 3:
            cw[1] = chuan_hoa_dau_tu_tieng_viet(cw[1])
        words[index] = ''.join(cw)
    return ' '.join(words)

def remove_url(text):
    return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)


stop_words = ['đã không', 'gần hết', 'tỏ ra', 'nói nhỏ', 'thúng thắng', 'từ loại', 'bao nhiêu', 'ăn làm', 'phỉ phui', 'chứ như', 'vung thiên địa', 'sang sáng', 'tại đâu', 'ông từ', 'giữa lúc', 'giờ đây', 'câu hỏi', 'không điều kiện', 'khẳng định', 'chốc chốc', 'lấy ra', 'nước xuống', 'nói là', 'sau đó', 'là phải', 'về không', 'dành dành', 'làm tăng', 'có tháng', 'tất cả bao nhiêu', 'nhìn theo', 'ơ kìa', 'cho được', 'ầu ơ', 'trong này', 'ối giời', 'tránh khỏi', 'ứ hự', 'chẳng nữa', 'cần số', 'phải rồi', 'đã thế', 'khó chơi', 'ờ ờ', 'sẽ hay', 'đưa chuyện', 'lượng số', 'cơ cùng', 'cho rằng', 'lúc này', 'quan trọng', 'ăn chung', 'vài điều', 'đang tay', 'lòng không', 'tới nơi', 'chết thật', 'cha chả', 'tăng cấp', 'ý chừng', 'đưa em', 'căn tính', 'chắc người', 'này nọ', 'rén bước', 'mỗi lúc', 'căn cắt', 'bất kể', 'ai nấy', 'ba ngày', 'bất quá', 'ráo cả', 'chu cha', 'bằng nào', 'đủ nơi', 'thực vậy', 'tại nơi', 'tha hồ', 'ăn hỏi', 'sử dụng', 'cảm ơn', 'ào vào', 'duy chỉ', 'đâu đây', 'ngộ nhỡ', 'vài nơi', 'biết mình', 'thường tại', 'trong mình', 'ô kìa', 'trước đây', 'vừa lúc', 'đâu cũng', 'thời điểm', 'từng ấy', 'ở được', 'cùng cực', 'khó nghĩ', 'vùng nước', 'quá tuổi', 'cật sức', 'thiếu điểm', 'dạ khách', 'chắc ăn', 'lần khác', 'tột cùng', 'tuần tự', 'những là', 'tự ý', 'bởi thế', 'thục mạng', 'trước ngày', 'tuốt tuồn tuột', 'trong ngoài', 'hiện nay', 'dù cho', 'thuộc bài', 'nữa khi', 'chịu chưa', 'không hay', 'thật sự', 'thà rằng', 'đặt mức', 'thậm từ', 'nhằm vào', 'dù sao', 'như không', 'bấy lâu nay', 'tuyệt nhiên', 'ngày đến', 'thích ý', 'thế sự', 'nghe chừng', 'đúng ngày', 'bộ thuộc', 'để giống', 'chưa dễ', 'ông nhỏ', 'thấy tháng', 'ba họ', 'vì chưng', 'càng hay', 'lấy có', 'tự lượng', 'thích tự', 'cơ mà', 'thật ra', 'thích cứ', 'ra ngôi', 'chuyển tự', 'ở đây', 'xon xón', 'dẫu rằng', 'ra tay', 'thường thôi', 'vì rằng', 'bất kì', 'xin gặp', 'thuần ái', 'lúc đi', 'đủ số', 'dễ thấy', 'nhờ đó', 'hơn là', 'thoạt nghe', 'ví phỏng', 'mà lại', 'nhanh lên', 'người khách', 'quả là', 'chưa dùng', 'cứ điểm', 'mỗi lần', 'lượng từ', 'nói riêng', 'khác nào', 'trời đất ơi', 'vị tất', 'bỏ mình', 'nói khó', 'quá mức', 'vèo vèo', 'từ tại', 'cuối cùng', 'phải cách', 'nhận nhau', 'ngày này', 'đáng lý', 'trước khi', 'sở dĩ', 'do vì', 'thường tính', 'đúng với', 'chung cho', 'mà không', 'phải biết', 'ái chà', 'hết nói', 'đâu đâu', 'chành chạnh', 'bỗng nhiên', 'có chăng là', 'ba tăng', 'trừ phi', 'ông tạo', 'như quả', 'nhất nhất', 'đưa tay', 'ngôi thứ', 'về phần', 'trệu trạo', 'sang năm', 'tấm bản', 'để phần', 'bỏ lại', 'từ đó', 'vừa mới', 'sì sì', 'thậm cấp', 'buổi sớm', 'bỏ mất', 'hay hay', 'gây giống', 'hay tin', 'nơi nơi', 'tại đây', 'hết của', 'dễ gì', 'tính cách', 'vâng vâng', 'chùn chũn', 'con nhà', 'gặp khó khăn', 'đều nhau', 'đại loại', 'nếu như', 'một khi', 'trong số', 'qua ngày', 'không ai', 'nói lại', 'riêng từng', 'nghĩ xa', 'lời nói', 'chứ không phải', 'lần tìm', 'trước tiên', 'cả người', 'trong vùng', 'tới gần', 'quả thế', 'thường khi', 'ông ấy', 'tháng ngày', 'xa xả', 'dễ dùng', 'ví bằng', 'chung quy', 'lấy làm', 'thấp thỏm', 'cây nước', 'cô ấy', 'đặc biệt', 'nào là', 'vào khoảng', 'kể như', 'tạo ra', 'dầu sao', 'về nước', 'nhón nhén', 'thích thuộc', 'sáng rõ', 'lại nữa', 'thực hiện', 'chưa từng', 'bấy nay', 'cấp số', 'đặt làm', 'nhớ ra', 'vung tàn tán', 'tắp lự', 'chung cuộc', 'từ khi', 'tuy có', 'có thể', 'như thế nào', 'ối dào', 'dễ như chơi', 'lên nước', 'lấy thế', 'lên số', 'cho tới', 'chứ còn', 'trả của', 'đến thế', 'gì gì', 'trước nay', 'thảo hèn', 'lúc đó', 'nhận việc', 'mang mang', 'không những', 'nào phải', 'trước đó', 'lớn nhỏ', 'thì thôi', 'tuổi cả', 'ra ý', 'quá tin', 'tuy rằng', 'dễ ngươi', 'con dạ', 'để không', 'cứ như', 'bên cạnh', 'tò te', 'chịu tốt', 'không kể', 'nức nở', 'lấy được', 'bỏ xa', 'lấy giống', 'tự tính', 'đến khi', 'vừa rồi', 'chết tiệt', 'sau cùng', 'cao thế', 'sao đang', 'qua chuyện', 'chỉ là', 'cả ăn', 'ba bản', 'ngồi bệt', 'làm dần dần', 'mang nặng', 'rồi đây', 'ăn sáng', 'cả nghĩ', 'cho đến khi', 'tình trạng', 'phần nào', 'tanh tanh', 'không gì', 'đưa cho', 'gì đó', 'sao bằng', 'ra gì', 'bước tới', 'tiếp tục', 'lấy cả', 'chung cục', 'xem ra', 'vậy mà', 'nhằm khi', 'trả ngay', 'có người', 'lên cao', 'phần việc', 'thuộc lại', 'hết cả', 'bất thình lình', 'trực tiếp', 'ấy là', 'ngay lập tức', 'ở vào', 'ai đó', 'cùng tuổi', 'dù rằng', 'vốn dĩ', 'bởi ai', 'thốt nhiên', 'từng phần', 'bằng người', 'số người', 'lại người', 'vài nhà', 'nhờ có', 'khi trước', 'hay sao', 'nữa rồi', 'bấy lâu', 'đồng thời', 'dở chừng', 'đánh giá', 'tìm bạn', 'tên họ', 'mất còn', 'khác nhau', 'dẫu mà', 'ngồi sau', 'chỉ tên', 'ngồi trệt', 'lên ngôi', 'dùng hết', 'vào đến', 'cũng vậy thôi', 'nước ăn', 'cho nên', 'phía bên', 'ăn cuộc', 'nói lên', 'biết đâu đấy', 'đáo để', 'giờ đến', 'đang thì', 'liên quan', 'nhiên hậu', 'nếu có', 'tha hồ chơi', 'ngõ hầu', 'từng nhà', 'lần sang', 'chú dẫn', 'đủ dùng', 'chắc hẳn', 'được lời', 'văng tê', 'ái dà', 'chớ không', 'chính điểm', 'dễ sợ', 'chao ôi', 'khi nên', 'bằng ấy', 'như chơi', 'ôi chao', 'họ xa', 'cật lực', 'cụ thể là', 'phải lời', 'chăng nữa', 'đầy năm', 'có số', 'ơi là', 'lúc khác', 'nghe không', 'con tính', 'đầu tiên', 'sáng thế', 'thốc tháo', 'thế ra', 'vậy thì', 'còn về', 'ngay cả', 'hết ý', 'xuất hiện', 'chưa chắc', 'mọi giờ', 'nhất mực', 'sao bản', 'sắp đặt', 'làm lòng', 'ăn ngồi', 'vậy ư', 'chứ gì', 'xử lý', 'vừa khi', 'nhất luật', 'trên bộ', 'bấy chầy', 'lại quả', 'tà tà', 'cơ hồ', 'nhỏ người', 'làm nên', 'bây bẩy', 'nếu vậy', 'người khác', 'tiếp đó', 'phía dưới', 'biết đâu chừng', 'dạ dài', 'còn nữa', 'có cơ', 'tôi con', 'quá lời', 'cách đều', 'để đến nỗi', 'thế nên', 'xa xa', 'hoàn toàn', 'mở mang', 'nhất tâm', 'vài người', 'phải khi', 'vô luận', 'thời gian tính', 'sáng ý', 'thanh không', 'một lúc', 'nói phải', 'chuyển đạt', 'đầy tuổi', 'tay quay', 'chung quy lại', 'chắc chắn', 'bao giờ', 'từ căn', 'thái quá', 'lấy vào', 'chứ lị', 'biết việc', 'giữ lấy', 'đưa tới', 'tiện thể', 'khi nào', 'như vậy', 'vừa qua', 'veo veo', 'cho biết', 'ngôi nhà', 'những ai', 'nên tránh', 'đã đủ', 'tuy vậy', 'nhất thiết', 'ăn chắc', 'không có gì', 'biết bao nhiêu', 'đều bước', 'giờ lâu', 'bỏ việc', 'đại phàm', 'lại ăn', 'qua đi', 'hoặc là', 'ngay bây giờ', 'làm thế nào', 'nhất định', 'nghe thấy', 'trước tuổi', 'mà vẫn', 'tăm tắp', 'về tay', 'ạ ơi', 'nhận được', 'phía trước', 'chỉ có', 'tránh ra', 'ra người', 'không đầy', 'nghe hiểu', 'phía trên', 'lần lần', 'tỏ vẻ', 'ba ngôi', 'phía bạn', 'trong khi', 'thì ra', 'đây này', 'bỏ riêng', 'lúc lâu', 'bản ý', 'bấy giờ', 'nghe được', 'khác khác', 'cùng tột', 'coi bộ', 'bán thế', 'ô hay', 'tên tự', 'qua khỏi', 'đã vậy', 'chính bản', 'ít nhiều', 'đưa xuống', 'bỗng chốc', 'quay lại', 'không bao lâu', 'không cùng', 'nào đó', 'vẫn thế', 'hay nói', 'còn như', 'dễ thường', 'ngày xửa', 'vâng ý', 'dùng đến', 'mọi khi', 'nhờ chuyển', 'ngay tức thì', 'khó thấy', 'ngay khi đến', 'nhận biết', 'ngay từ', 'ra đây', 'chưa có', 'cái đã', 'một cách', 'của ngọt', 'do vậy', 'đánh đùng', 'quan tâm', 'lên cơn', 'bất đồ', 'bỏ không', 'ráo trọi', 'làm lấy', 'đưa vào', 'sốt sột', 'mọi thứ', 'hay nhỉ', 'khó khăn', 'ồ ồ', 'sự thế', 'lấy xuống', 'ra chơi', 'cho tới khi', 'hầu hết', 'nói rõ', 'xuất kì bất ý', 'nhà làm', 'nhận ra', 'đưa ra', 'nữa là', 'nếu cần', 'thời gian', 'thế thôi', 'đâu phải', 'qua tay', 'đâu đó', 'oai oái', 'tại đó', 'mới hay', 'nhà ngươi', 'lúc đến', 'không thể', 'nhìn nhận', 'thật vậy', 'trong lúc', 'biết đâu', 'công nhiên', 'tuy thế', 'phải lại', 'vị trí', 'bỗng dưng', 'chưa kể', 'số loại', 'tránh tình trạng', 'của tin', 'họ gần', 'xin vâng', 'thế thế', 'đây đó', 'nhận làm', 'tập trung', 'nhớ bập bõm', 'chăn chắn', 'người nhận', 'nước lên', 'không phải không', 'dẫu sao', 'chung ái', 'tức thì', 'cụ thể như', 'bài bác', 'giống như', 'suýt nữa', 'từ ái', 'đặt ra', 'phỏng như', 'có đáng', 'nhận thấy', 'trả trước', 'hơn trước', 'tìm việc', 'mỗi một', 'nếu được', 'ở như', 'chứ không', 'những như', 'chí chết', 'bỏ nhỏ', 'chưa bao giờ', 'giống người', 'hết chuyện', 'dùng làm', 'ứ ừ', 'cùng ăn', 'nhất loạt', 'xa tắp', 'luôn cả', 'lần theo', 'không cần', 'lấy ráo', 'đến lời', 'phải cái', 'tha hồ ăn', 'sự việc', 'thực sự', 'điểm gặp', 'bỗng không', 'nhìn chung', 'làm được', 'ngày càng', 'không bán', 'điều gì', 'ít hơn', 'tính người', 'cuối điểm', 'dạ bán', 'chắc lòng', 'vào vùng', 'tuốt tuột', 'dễ khiến', 'đến thì', 'tiếp theo', 'ngăn ngắt', 'để lại', 'vâng dạ', 'cũng như', 'đã là', 'bất ngờ', 'hãy còn', 'nói ra', 'giảm thấp', 'nói thêm', 'ví thử', 'ít ra', 'chắc vào', 'nước cùng', 'bây chừ', 'chứ sao', 'bài cái', 'ừ ào', 'thuộc từ', 'từng cái', 'trước kia', 'anh ấy', 'ăn chịu', 'tự khi', 'những muốn', 'ngày qua', 'nhiệt liệt', 'à ơi', 'bằng không', 'nghĩ tới', 'có ngày', 'tìm hiểu', 'khó biết', 'bất chợt', 'người hỏi', 'toé khói', 'làm ngay', 'giờ này', 'thương ôi', 'vì vậy', 'có phải', 'như thể', 'đến cùng cực', 'như thế', 'xiết bao', 'bất tử', 'căn cái', 'xềnh xệch', 'như trước', 'làm sao', 'ít thấy', 'dài ra', 'cao xa', 'có thế', 'sa sả', 'quá trình', 'phải giờ', 'tự cao', 'thường hay', 'nhận họ', 'yêu cầu', 'làm đúng', 'là nhiều', 'vừa vừa', 'nước bài', 'khá tốt', 'đại để', 'tấm các', 'cái họ', 'cô tăng', 'ví dù', 'sáng ngày', 'vào gặp', 'ngày giờ', 'một vài', 'cần cấp', 'như tuồng', 'khác xa', 'dù dì', 'ngày xưa', 'điểm đầu tiên', 'lên mạnh', 'bây nhiêu', 'thường sự', 'có nhiều', 'ô kê', 'kể cả', 'đến nỗi', 'đều đều', 'cứ việc', 'phải chi', 'hay làm', 'khác gì', 'thường xuất hiện', 'bởi thế cho nên', 'ngoài ra', 'ý da', 'thế thì', 'cho đến nỗi', 'biết chắc', 'gây thêm', 'từng giờ', 'vì thế', 'nhìn lại', 'nghe rõ', 'bởi đâu', 'khoảng không', 'vấn đề quan trọng', 'tức tốc', 'tính căn', 'ngày nọ', 'đáng số', 'sẽ biết', 'cơ hội', 'trong đó', 'ắt hẳn', 'thanh điểm', 'nào đâu', 'điểm chính', 'khác thường', 'đưa tin', 'phương chi', 'úi dào', 'quả thật', 'nói xa', 'chung chung', 'vô hình trung', 'ăn người', 'vùng lên', 'nhung nhăng', 'thường bị', 'thuộc cách', 'biết thế', 'bị vì', 'thế lại', 'cơ dẫn', 'nhân dịp', 'bỏ bà', 'lấy lý do', 'lâu ngày', 'phù hợp', 'đáng lí', 'mọi nơi', 'cho nhau', 'có điều kiện', 'bên có', 'chớ như', 'ngày nào', 'nhất quyết', 'phải chăng', 'có nhà', 'đến hay', 'thấp cơ', 'qua lần', 'bộ điều', 'mà cả', 'có chăng', 'cao thấp', 'nói với', 'làm vì', 'giá trị', 'nên người', 'ngoài xa', 'thêm vào', 'lâu các', 'không để', 'thế đó', 'khỏi nói', 'cho chắc', 'cả thảy', 'làm gì', 'buổi mới', 'từ tính', 'nhớ lại', 'một ít', 'bởi vậy', 'giữ ý', 'cùng với', 'trực tiếp làm', 'tới mức', 'hay đâu', 'chúng tôi', 'chú mày', 'nghe như', 'chọn ra', 'âu là', 'bây giờ', 'đến ngày', 'tự vì', 'là cùng', 'nhìn xuống', 'đó đây', 'xăm xăm', 'làm riêng', 'đến nay', 'tăng chúng', 'tháng tháng', 'cái đó', 'ngày ấy', 'lượng cả', 'bao nả', 'có họ', 'mở ra', 'thoạt nhiên', 'xăm xúi', 'lúc nào', 'nói qua', 'đáng lẽ', 'ít nhất', 'vài tên', 'nhỡ ra', 'bập bõm', 'do đó', 'không còn', 'ít có', 'như sau', 'thanh điều kiện', 'hết ráo', 'số là', 'lần nào', 'hay là', 'hỏi lại', 'thường đến', 'tốt mối', 'rõ thật', 'thứ đến', 'bởi nhưng', 'đưa đến', 'ít khi', 'thật thà', 'thực tế', 'quá tay', 'chú mình', 'ừ ừ', 'việc gì', 'không tính', 'bởi tại', 'tạo điều kiện', 'có ai', 'chung nhau', 'tạo ý', 'gần bên', 'làm lại', 'rất lâu', 'bỗng nhưng', 'có vẻ', 'ngày tháng', 'có dễ', 'kể từ', 'nhà việc', 'phần nhiều', 'đến xem', 'sau đây', 'đủ điều', 'nước nặng', 'khó nghe', 'tênh tênh', 'dễ ăn', 'cao số', 'phải người', 'đã lâu', 'a lô', 'có ăn', 'bởi chưng', 'bản riêng', 'không bao giờ', 'vượt khỏi', 'được tin', 'thì phải', 'đúng tuổi', 'từ từ', 'lời chú', 'càng càng', 'nghe đâu như', 'bỗng đâu', 'nói toẹt', 'sau hết', 'để được', 'như trên', 'hay không', 'cô quả', 'luôn tay', 'thật chắc', 'theo tin', 'đơn vị', 'là là', 'quá đáng', 'rõ là', 'nhà tôi', 'ít thôi', 'chú khách', 'ngay thật', 'nói đủ', 'phải tay', 'lại bộ', 'cá nhân', 'tất cả', 'nhanh tay', 'nếu không', 'hơn cả', 'có khi', 'những khi', 'không phải', 'phỏng tính', 'duy có', 'thay đổi tình trạng', 'hỏi xem', 'có chứ', 'lúc trước', 'không ngoài', 'quan trọng vấn đề', 'khó làm', 'ngay lúc này', 'cho hay', 'tên chính', 'phần sau', 'bằng như', 'tông tốc', 'chịu lời', 'lấy lại', 'cách bức', 'số phần', 'lấy số', 'rồi sao', 'ba cùng', 'vả lại', 'cơ chỉ', 'tốt ngày', 'tự tạo', 'rút cục', 'ở năm', 'như ai', 'giá trị thực tế', 'tạo cơ hội', 'mọi việc', 'gây cho', 'bước khỏi', 'thà là', 'cảm thấy', 'rồi ra', 'chứ ai', 'xem lại', 'từng đơn vị', 'chui cha', 'lấy để', 'được cái', 'chầm chập', 'tất thảy', 'thi thoảng', 'với lại', 'chẳng lẽ', 'thỉnh thoảng', 'tù tì', 'lại cái', 'dễ nghe', 'có ý', 'cả tin', 'lại nói', 'thêm chuyện', 'chúng ta', 'ngồi không', 'bỗng thấy', 'phải không', 'thế mà', 'cùng nhau', 'cũng nên', 'phần lớn', 'coi mòi', 'trước nhất', 'dễ đâu', 'đến giờ', 'để lòng', 'cả thể', 'có được', 'ăn quá', 'tuy là', 'từ thế', 'so với', 'chớ gì', 'nhà chung', 'nhớ lấy', 'bội phần', 'đành đạch', 'đến cùng', 'làm cho', 'tuy đã', 'cho tin', 'gặp phải', 'cho đến', 'thực hiện đúng', 'tới thì', 'ăn hết', 'xăm xắm', 'chùn chùn', 'thật lực', 'làm mất', 'chung qui', 'ớ này', 'bay biến', 'bập bà bập bõm', 'tránh xa', 'ở lại', 'song le', 'từ ấy', 'một số', 'tất tật', 'rồi nữa', 'được nước', 'chợt nhìn', 'nhất là', 'cả nhà', 'ngay tức khắc', 'ừ thì', 'ngay lúc', 'lần trước', 'cụ thể', 'có đâu', 'gần đây', 'cực lực', 'sau cuối', 'đến nơi', 'đảm bảo', 'lâu nay', 'từ nay', 'lên xuống', 'rồi thì', 'lớn lên', 'biết bao', 'buổi làm', 'mà thôi', 'mỗi người', 'mọi người', 'tại tôi', 'tất tần tật', 'thế à', 'bởi sao', 'phè phè', 'ngày cấp', 'thế nào', 'là vì', 'lại đây', 'đến cả', 'vô vàn', 'sau này', 'ăn trên', 'quay đi', 'tháng năm', 'chưa tính', 'tốt hơn', 'mới rồi', 'hỏi xin', 'khó tránh', 'tự ăn', 'tốt bạn', 'làm tin', 'thế chuẩn bị', 'chính là', 'cô mình', 'ít biết', 'lần này', 'đặt mình', 'trả lại', 'tại vì', 'quá bán', 'đến đâu', 'như là', 'đúng ra', 'quay số', 'từ điều', 'chợt nghe', 'bấy chừ', 'bước đi', 'còn thời gian', 'cả ngày', 'chọn bên', 'lại thôi', 'dùng cho', 'nhằm lúc', 'người người', 'vậy nên', 'phía sau', 'bất cứ', 'thốt thôi', 'chớ chi', 'mỗi ngày', 'ào ào', 'không được', 'thì giờ', 'gần như', 'ơ hay', 'rồi sau', 'mọi lúc', 'nếu mà', 'xuất kỳ bất ý', 'sang tay', 'tin thêm', 'cơ chừng', 'a ha', 'đối với', 'gây ra', 'cách nhau', 'tuốt luốt', 'vung tán tàn', 'vượt quá', 'tính phỏng', 'từng thời gian', 'luôn luôn', 'chúng ông', 'thế thường', 'nói tốt', 'lại còn', 'ren rén', 'lại làm', 'biết chừng nào', 'bỏ cha', 'cái gì', 'rồi tay', 'xa cách', 'làm bằng', 'ngọn nguồn', 'thanh thanh', 'ối giời ơi', 'quá thì', 'xảy ra', 'sau chót', 'trong ấy', 'tại lòng', 'thanh chuyển', 'trước sau', 'vạn nhất', 'tối ư', 'chỉ chính', 'tựu trung', 'chẳng phải', 'xem số', 'thường thường', 'hay biết', 'nào cũng', 'cho ăn', 'có điều', 'đưa về', 'đặt để', 'với nhau', 'trước hết', 'rằng là', 'thay đổi', 'theo bước', 'tốt bộ', 'bằng vào', 'bán cấp', 'lấy thêm', 'đến bao giờ', 'cao sang', 'riu ríu', 'vào lúc', 'thật tốt', 'khi khác', 'cho về', 'vài ba', 'nghe nhìn', 'thanh tính', 'áng như', 'chơi họ', 'hỗ trợ', 'vâng chịu', 'xa gần', 'bằng nấy', 'chẳng những', 'bởi vì', 'bỏ quá', 'lên đến', 'thứ bản', 'đến lúc', 'ít nữa', 'phải như', 'thì là', 'giảm chính', 'gần đến', 'nên chi', 'nghe tin', 'cao lâu', 'thế là', 'lấy sau', 'gần ngày', 'tìm cách', 'phỏng theo', 'ăn riêng', 'ăn về', 'thành ra', 'đáng kể', 'chăng chắc', 'các cậu', 'thình lình', 'tuy nhiên', 'rồi xem', 'bản thân', 'phía trong', 'bà ấy', 'nên chăng', 'cùng chung', 'nhìn thấy', 'kể tới', 'đến điều', 'dữ cách', 'cần gì', 'sao vậy', 'thật là', 'có chuyện', 'giờ đi', 'bấy nhiêu', 'nói thật', 'xa nhà', 'bắt đầu', 'sao cho', 'chính thị', 'ở trên', 'không nhận', 'nên làm', 'dần dần', 'về sau', 'mang lại', 'lần sau', 'nghĩ ra', 'khoảng cách', 'buổi ngày', 'đây rồi', 'ít quá', 'là thế nào', 'thực ra', 'một cơn', 'nhằm để', 'ngày ngày', 'biết mấy', 'nếu thế', 'nghe đâu', 'làm tôi', 'đặt trước', 'trếu tráo', 'tăng thêm', 'cũng thế', 'làm như', 'phăn phắt', 'than ôi', 'mọi sự', 'nhất sinh', 'chuẩn bị', 'ráo nước', 'tắp tắp', 'dạ con', 'số cụ thể', 'ăn tay', 'ông ổng', 'ra điều', 'nước quả', 'ngay khi', 'năm tháng', 'bất giác', 'nhưng mà', 'dài lời', 'nói ý', 'là ít', 'chị bộ', 'đã hay', 'cũng vậy', 'ở nhờ', 'nghe trực tiếp', 'ngoài này', 'bất quá chỉ', 'làm tại', 'thảo nào', 'em em', 'cho đang', 'quá ư', 'rốt cục', 'nhất đán', 'ra bài', 'trở thành', 'nhất tề', 'răng răng', 'thành thử', 'cổ lai', 'thật quả', 'ắt là', 'loại từ', 'thốt nói', 'xa tanh', 'chứ lại', 'nói chung', 'làm theo', 'nhân tiện', 'không chỉ', 'lại giống', 'không dùng', 'tại sao', 'cả nghe', 'quay bước', 'bất kỳ', 'phỏng nước', 'không biết', 'thiếu gì', 'á à', 'không có', 'xoành xoạch', 'đâu có', 'biết được', 'rốt cuộc', 'qua thì', 'bên bị', 'lúc sáng', 'bắt đầu từ', 'khó nói', 'như ý', 'đâu nào', 'thời gian sử dụng', 'nặng mình', 'nghe nói', 'ra lời', 'chắc dạ', 'quá nhiều', 'sau sau', 'tạo nên', 'chia sẻ', 'thanh ba', 'ngày rày', 'ra vào', 'số cho biết', 'ô hô', 'thêm giờ', 'theo như', 'con con', 'ít lâu', 'điều kiện', 'vậy ra', 'ý hoặc', 'những lúc', 'ở đó', 'như nhau', 'cao răng', 'vậy là', 'chịu ăn', 'bằng nhau', 'rón rén', 'để mà', 'à này', 'sau nữa', 'làm ra', 'tuổi tôi', 'nói đến', 'nói trước', 'bị chú', 'hiện tại', 'úi chà', 'đâu như', 'cách không', 'hết rồi', 'khó mở', 'chết nỗi', 'ừ nhé', 'đến tuổi', 'đại nhân', 'không cứ', 'mở nước', 'ra sao', 'lý do', 'thôi việc', 'quá bộ', 'bán dạ', 'nhược bằng', 'chị ấy', 'bất nhược', 'trên dưới', 'chính giữa', 'cũng được', 'để cho', 'thậm chí', 'cái ấy', 'ắt phải', 'bỏ mẹ', 'dần dà', 'khi không', 'nhiều ít', 'nước đến', 'số thiếu', 'tít mù', 'cả năm', 'chưa cần', 'vì sao', 'tăng thế', 'nghĩ đến', 'tìm ra', 'quả vậy', 'qua lại', 'biết trước', 'đầy phè', 'ra lại', 'nghiễm nhiên', 'dạ dạ', 'ba ba', 'giống nhau', 'tên cái', 'bỏ cuộc', 'đủ điểm', 'ôi thôi', 'dưới nước', 'nhất thì', 'tấn tới', 'lâu lâu', 'thấp xuống', 'như thường', 'nói bông', 'chớ kể', 'giảm thế', 'bất luận', 'nghe lại', 'quá giờ', 'làm tắp lự', 'bằng được', 'nào hay', 'cấp trực tiếp', 'bao lâu', 'vả chăng', 'từ giờ', 'nghe ra', 'tin vào', 'bỏ ra', 'bài bỏ', 'nhờ nhờ', 'mang về', 'nặng căn', 'tính từ', 'hơn nữa', 'ai ai', 'dễ sử dụng', 'mới đây', 'vấn đề', 'chúng mình', 'gần xa', 'vô kể', 'nặng về', 'ra bộ', 'tốc tả', 'tăng giảm', 'không khỏi', 'người mình', 'thường số', 'cao ráo', 'nghĩ lại', 'cu cậu', 'bản bộ', 'sớm ngày', 'ắt thật', 'cho thấy', 'bằng cứ', 'hơn hết', 'lúc ấy', 'cho rồi', 'cóc khô', 'nhà ngoài', 'đến gần', 'nhà khó']

stop_words1={'nhưng', 'trả', 'nhóm', 'vậy', 'liên_kết', 'thẩy', 'cấp', 'vừa', 'ơ', 'trước', 'mọi', 'nhận', 'lời', 'và', 'amen', 'chậc', 'cách', 'trên', 'bài', 'ngôi', 'trệt', 'nói', 'hai', 'buổi', 'thấp', 'loài', 'tạo', 'thốc', 'vụt', 'không', 'thường', 'chính', 'cùng', 'điểm', 'bệt', 'nếu', 'ái', 'oái', 'bản', 'giảm', 'bển', 'giữa', 'bông', 'sắp', 'giờ', 'ngay', 'cái', 'khó', 'thế', 'bỗng', 'tránh', 'rõ', 'thuần', 'phía', 'bên', 'hoa', 'chú', 'tới', 'bước', 'bà', 'chỉ', 'ờ', 'chung', 'nghĩ', 'tỉnh', 'tin', 'rằng', 'ngày', 'căn', 'gần', 'ngoải', 'sáng', 'nóc', 'mối', 'được', 'càng', 'rồi', 'chị', 'cuộc', 'nặng', 'con', 'sang', 'bức', 'nguồn', 'giữ', 'loại', 'điều', 'nhất', 'phót', 'bớ', 'thoắt', 'ngoài', 'cần', 'từng', 'lúc', 'bằng', 'vẫn', 'cơ', 'này', 'ồ', 'thực_vật', 'tấn', 'ơi', 'đúng', 'dạ', 'dễ', 'bị', 'vài', 'bác', 'ủa', 'thỏm', 'cũng', 'nền', 'nhằm', 'ngồi', 'xuống', 'ấy', 'mợ', 'nó', 'hãy', 'phè', 'đã', 'tanh', 'ớ', 'gây', 'do', 'trỏng', 'dân_số', 'chăng', 'dẫn', 'khỏi', 'dì', 'xoét', 'một', 'đều', 'dành', 'lớn', 'ư', 'lại', 'rất', 'cơn', 'để', 'sất', 'nước', 'lên', 'khác', 'anh', 'làm', 'đang', 'phỏng', 'nhé', 'như', 'nhau', 'tên', 'xuể', 'mất', 'đầu_tiên', 'còn', 'thuộc', 'qua', 'của', 'cứ', 'tôi', 'thộc', 'mô_tả', 'chọn', 'có', 'duy', 'mà', 'đưa', 'hỏi', 'chiếc', 'thì', 'mang', 'mạnh', 'nhìn', 'nhỉ', 'thím', 'trong', 'ắt', 'tắp', 'bán', 'thật', 'xệp', 'ở', 'dùng', 'riệt', 'đây', 'thêm', 'ừ', 'hơn', 'xoẳn', 'toẹt', 'răng', 'tuổi', 'à', 'khá', 'sì', 'từ', 'năm', 'miêu_tả', 'vào', 'quận', 'chủn', 'các', 'xem', 'tay', 'thứ', 'tốt', 'phốc', 'mỗi', 'cho', 'chuyện', 'vở', 'cả', 'riêng', 'thửa', 'việc', 'béng', 'thốt', 'thanh', 'người', 'đủ', 'dưới', 'vùng', 'đầy', 'phóc', 'gặp', 'vì', 'ai', 'ngọn', 'chúng', 'tênh', 'thấy', 'cậu', 'cuốn', 'tọt', 'vượt', 'cao', 'đặt', 'biết', 'mở', 'sẽ', 'rích', 'khi', 'cây', 'sự', 'phứt', 'phắt', 'số', 'xa', 'thoạt', 'khiến', 'introduction', 'dài', 'hiểu', 'veo', 'ạ', 'rén', 'lòng', 'rứa', 'mức', 'với', 'cuối', 'sớm', 'tham_khảo', 'úi', 'nấy', 'nên', 'ráo', 'ử', 'bộ', 'gì', 'toà', 'gồm', 'ngươi', 'tại', 'nhỏ', 'trển', 'tìm', 'sau', 'dữ', 'nhớ', 'nghe', 'chợt', 'thà', 'chuyển', 'em', 'về', 'đó', 'vèo', 'mới', 'khách', 'cha', 'bỏ', 'đạt', 'nhà', 'á', 'so', 'chắc', 'thiếu', 'chịu', 'xoẹt', 'đâu', 'thậm', 'ba', 'lâu', 'bèn', 'dù', 'đến', 'nọ', 'họ', 'nớ', 'nhờ', 'theo', 'nữa', 'hoặc', 'chớ', 'bấy', 'nào', 'áng', 'nay', 'mình', 'alô', 'nơi', 'lấy', 'bạn', 'xin', 'ông', 'chơi', 'tớ', 'là', 'lượng', 'ăn', 'quả', 'thích', 'phải', 'choa', 'ý', 'tuy', 'khoảng', 'ra', 'hết', 'kể', 'chỉn', 'giống', 'tột', 'vâng', 'dào', 'đáng', 'thôi', 'ổng', 'nghỉm', 'tăng', 'muốn', 'cô', 'tính', 'bởi', 'ngọt', 'lần', 'tháng', 'chứ', 'luôn', 'hay', 'những', 'thể_loại', 'tấm', 'phần', 'nhanh', 'nghen', 'chưa', 'sao', 'quay', 'dẫu', 'thếch', 'phụt', 'ào', 'ít', 'pho', 'rày', 'khoa_học', 'nhiều', 'tự', 'suýt', 'chú_thích', 'quá','diễn','-','1', '2','nè','ừa','Ủa','mấy'}



def xoastopword(text):
    text = text.split()
    text = [word for word in text if word not in stop_words]
    text = ' '.join(text)
    return text
def xoastopword1(text):
    text = text.split()
    text = [word for word in text if word not in stop_words1]
    text = ' '.join(text)
    return text



def preprocess_text(text):
    # Loại bỏ URL
    cleaned_text = remove_url(text)
    text2 =  remove_icon(cleaned_text)
    text3 = text2.split()
    text4 = ' '.join(abbreviations.get(word, word) for word in text3)
    text5 = text4.split()
    text6 = ' '.join(english.get(word, word) for word in text5)
    text7 = text6.split()
    text8 = ' '.join(sentiment_words.get(word, word) for word in text7)
    # Unicode normalization
    cleaned_text = convert_unicode(text8)
    # # Chuẩn hóa dấu câu
    cleaned_text1 = chuan_hoa_dau_cau_tieng_viet(cleaned_text)
    # # Chuẩn hóa dấu từ
    cleaned_text2 = chuan_hoa_dau_tu_tieng_viet(cleaned_text1)
    # Chuyển về chữ thường
    cleaned_text3 = cleaned_text2.lower()

    # Tokenization cho tiếng Việt
    cleaned_text4 = ViTokenizer.tokenize(cleaned_text3)
    # Loại bỏ khoảng trắng dư thừa
    cleaned_text5 = re.sub(r'\s+', ' ', cleaned_text4).strip()

    return cleaned_text5



