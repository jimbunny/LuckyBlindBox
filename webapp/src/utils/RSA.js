import JSEncrypt from 'jsencrypt'
 
/**
 * 对content进行RSA加密
 * @param {*}} content
 */
export function RSAEncrypt(content) {
  let encryptor = new JSEncrypt() // 创建加密对象实例
  // 公钥
  let pubKey = '-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCdGPI9URX1JLrNJLnkNoH/G4Og1eVcrO27dySbnjzkZGczL8XtTpZVussY7BmB1aZEvCnk5ZqNNbGWoTw364/mMmVLTDsN1gUlEP4KkHED+WjC9spOS2ieIDMlvrMH23Rnw7grIeCv73hkIBaf9h916E0gZ+nau8kiWJYSw9QRWwIDAQAB-----END PUBLIC KEY-----'
 
  encryptor.setPublicKey(pubKey) // 设置公钥
 
  return encryptor.encrypt(content) // 对内容进行加密, 可以在此打印下密文串
}