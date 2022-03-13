import java.security.MessageDigest;
import java.util.TreeMap;

public class CD {

    private static String toHex(byte[] bArr) {

		char[] hexDigits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
        int length = bArr.length;
        char[] cArr = new char[length * 2];
        int i = 0;
		
        for (byte b : bArr) {
            int i2 = i + 1;
            char[] cArr2 = hexDigits;
            cArr[i] = cArr2[(b >>> 4) & 15];
            i = i2 + 1;
            cArr[i2] = cArr2[b & 15];
        }
        return new String(cArr);
    }
    
    public static void main(String[] args) {
        TreeMap treeMap = new TreeMap();

        for(String s : args){
            int i = s.indexOf("=");
            treeMap.put(s.substring(0, i),s.substring(i+1,s.length()));
        }
        StringBuffer stringBuffer = new StringBuffer();
		for (Object str5 : treeMap.keySet()) {
			stringBuffer.append(str5);
			stringBuffer.append("=");
			stringBuffer.append((String) treeMap.get(str5));
			stringBuffer.append("&");
		}
		stringBuffer.append("aef2890665d884a3080971b4eca594d7");
		//System.out.println(stringBuffer.toString());
		try{
		MessageDigest md = MessageDigest.getInstance("MD5");
		md.update(stringBuffer.toString().getBytes("UTF-8"));
		System.out.println(toHex(md.digest()).toUpperCase());
		} catch (Exception e){}
    }
}