# AUTOMATICALLY GENERATED FILE - DO NOT EDIT
# TO REGENERATE: poe gen
# OR: uv run poe gen
from enum import Enum

from .. import rsid_py


class AlgoFlowEnum(str, Enum):
    All = 'AlgoFlow.All'
    FaceDetectionOnly = 'AlgoFlow.FaceDetectionOnly'
    PersonDetectionOnly = 'AlgoFlow.PersonDetectionOnly'
    PoseEstimationOnly = 'AlgoFlow.PoseEstimationOnly'
    BarcodeDecodingOnly = 'AlgoFlow.BarcodeDecodingOnly'
    BodyPartDetectionOnly = 'AlgoFlow.BodyPartDetectionOnly'
    SpoofOnly = 'AlgoFlow.SpoofOnly'
    RecognitionOnly = 'AlgoFlow.RecognitionOnly'

    def __str__(self):
        return f'{self.value}'

    def to_rsid_py(self) -> rsid_py.AlgoFlow:
        enum_map = {}
        enum_map['AlgoFlow.All'] = rsid_py.AlgoFlow.All
        enum_map['AlgoFlow.FaceDetectionOnly'] = rsid_py.AlgoFlow.FaceDetectionOnly
        enum_map['AlgoFlow.PersonDetectionOnly'] = rsid_py.AlgoFlow.PersonDetectionOnly
        enum_map['AlgoFlow.PoseEstimationOnly'] = rsid_py.AlgoFlow.PoseEstimationOnly
        enum_map['AlgoFlow.BarcodeDecodingOnly'] = rsid_py.AlgoFlow.BarcodeDecodingOnly
        enum_map['AlgoFlow.BodyPartDetectionOnly'] = rsid_py.AlgoFlow.BodyPartDetectionOnly
        enum_map['AlgoFlow.SpoofOnly'] = rsid_py.AlgoFlow.SpoofOnly
        enum_map['AlgoFlow.RecognitionOnly'] = rsid_py.AlgoFlow.RecognitionOnly
        return enum_map[self.value]

    @classmethod
    def from_rsid_py(cls, val: rsid_py.AlgoFlow) -> 'AlgoFlowEnum':
        enum_map = {}
        enum_map[rsid_py.AlgoFlow.All] = AlgoFlowEnum.All
        enum_map[rsid_py.AlgoFlow.FaceDetectionOnly] = AlgoFlowEnum.FaceDetectionOnly
        enum_map[rsid_py.AlgoFlow.PersonDetectionOnly] = AlgoFlowEnum.PersonDetectionOnly
        enum_map[rsid_py.AlgoFlow.PoseEstimationOnly] = AlgoFlowEnum.PoseEstimationOnly
        enum_map[rsid_py.AlgoFlow.BarcodeDecodingOnly] = AlgoFlowEnum.BarcodeDecodingOnly
        enum_map[rsid_py.AlgoFlow.BodyPartDetectionOnly] = AlgoFlowEnum.BodyPartDetectionOnly
        enum_map[rsid_py.AlgoFlow.SpoofOnly] = AlgoFlowEnum.SpoofOnly
        enum_map[rsid_py.AlgoFlow.RecognitionOnly] = AlgoFlowEnum.RecognitionOnly
        return enum_map[val]


class CameraRotationEnum(str, Enum):
    Rotation_0_Deg = 'CameraRotation.Rotation_0_Deg'
    Rotation_180_Deg = 'CameraRotation.Rotation_180_Deg'
    Rotation_90_Deg = 'CameraRotation.Rotation_90_Deg'
    Rotation_270_Deg = 'CameraRotation.Rotation_270_Deg'

    def __str__(self):
        return f'{self.value}'

    def to_rsid_py(self) -> rsid_py.CameraRotation:
        enum_map = {}
        enum_map['CameraRotation.Rotation_0_Deg'] = rsid_py.CameraRotation.Rotation_0_Deg
        enum_map['CameraRotation.Rotation_180_Deg'] = rsid_py.CameraRotation.Rotation_180_Deg
        enum_map['CameraRotation.Rotation_90_Deg'] = rsid_py.CameraRotation.Rotation_90_Deg
        enum_map['CameraRotation.Rotation_270_Deg'] = rsid_py.CameraRotation.Rotation_270_Deg
        return enum_map[self.value]

    @classmethod
    def from_rsid_py(cls, val: rsid_py.CameraRotation) -> 'CameraRotationEnum':
        enum_map = {}
        enum_map[rsid_py.CameraRotation.Rotation_0_Deg] = CameraRotationEnum.Rotation_0_Deg
        enum_map[rsid_py.CameraRotation.Rotation_180_Deg] = CameraRotationEnum.Rotation_180_Deg
        enum_map[rsid_py.CameraRotation.Rotation_90_Deg] = CameraRotationEnum.Rotation_90_Deg
        enum_map[rsid_py.CameraRotation.Rotation_270_Deg] = CameraRotationEnum.Rotation_270_Deg
        return enum_map[val]


class SecurityLevelEnum(str, Enum):
    High = 'SecurityLevel.High'
    Medium = 'SecurityLevel.Medium'
    Low = 'SecurityLevel.Low'

    def __str__(self):
        return f'{self.value}'

    def to_rsid_py(self) -> rsid_py.SecurityLevel:
        enum_map = {}
        enum_map['SecurityLevel.High'] = rsid_py.SecurityLevel.High
        enum_map['SecurityLevel.Medium'] = rsid_py.SecurityLevel.Medium
        enum_map['SecurityLevel.Low'] = rsid_py.SecurityLevel.Low
        return enum_map[self.value]

    @classmethod
    def from_rsid_py(cls, val: rsid_py.SecurityLevel) -> 'SecurityLevelEnum':
        enum_map = {}
        enum_map[rsid_py.SecurityLevel.High] = SecurityLevelEnum.High
        enum_map[rsid_py.SecurityLevel.Medium] = SecurityLevelEnum.Medium
        enum_map[rsid_py.SecurityLevel.Low] = SecurityLevelEnum.Low
        return enum_map[val]


class MatcherConfidenceLevelEnum(str, Enum):
    High = 'MatcherConfidenceLevel.High'
    Medium = 'MatcherConfidenceLevel.Medium'
    Low = 'MatcherConfidenceLevel.Low'

    def __str__(self):
        return f'{self.value}'

    def to_rsid_py(self) -> rsid_py.MatcherConfidenceLevel:
        enum_map = {}
        enum_map['MatcherConfidenceLevel.High'] = rsid_py.MatcherConfidenceLevel.High
        enum_map['MatcherConfidenceLevel.Medium'] = rsid_py.MatcherConfidenceLevel.Medium
        enum_map['MatcherConfidenceLevel.Low'] = rsid_py.MatcherConfidenceLevel.Low
        return enum_map[self.value]

    @classmethod
    def from_rsid_py(cls, val: rsid_py.MatcherConfidenceLevel) -> 'MatcherConfidenceLevelEnum':
        enum_map = {}
        enum_map[rsid_py.MatcherConfidenceLevel.High] = MatcherConfidenceLevelEnum.High
        enum_map[rsid_py.MatcherConfidenceLevel.Medium] = MatcherConfidenceLevelEnum.Medium
        enum_map[rsid_py.MatcherConfidenceLevel.Low] = MatcherConfidenceLevelEnum.Low
        return enum_map[val]


class StatusEnum(str, Enum):
    Ok = 'Status.Ok'
    Error = 'Status.Error'
    SerialError = 'Status.SerialError'
    SecurityError = 'Status.SecurityError'
    VersionMismatch = 'Status.VersionMismatch'
    CrcError = 'Status.CrcError'
    TooManySpoofs = 'Status.TooManySpoofs'
    NotSupported = 'Status.NotSupported'

    def __str__(self):
        return f'{self.value}'

    def to_rsid_py(self) -> rsid_py.Status:
        enum_map = {}
        enum_map['Status.Ok'] = rsid_py.Status.Ok
        enum_map['Status.Error'] = rsid_py.Status.Error
        enum_map['Status.SerialError'] = rsid_py.Status.SerialError
        enum_map['Status.SecurityError'] = rsid_py.Status.SecurityError
        enum_map['Status.VersionMismatch'] = rsid_py.Status.VersionMismatch
        enum_map['Status.CrcError'] = rsid_py.Status.CrcError
        enum_map['Status.TooManySpoofs'] = rsid_py.Status.TooManySpoofs
        enum_map['Status.NotSupported'] = rsid_py.Status.NotSupported
        return enum_map[self.value]

    @classmethod
    def from_rsid_py(cls, val: rsid_py.Status) -> 'StatusEnum':
        enum_map = {}
        enum_map[rsid_py.Status.Ok] = StatusEnum.Ok
        enum_map[rsid_py.Status.Error] = StatusEnum.Error
        enum_map[rsid_py.Status.SerialError] = StatusEnum.SerialError
        enum_map[rsid_py.Status.SecurityError] = StatusEnum.SecurityError
        enum_map[rsid_py.Status.VersionMismatch] = StatusEnum.VersionMismatch
        enum_map[rsid_py.Status.CrcError] = StatusEnum.CrcError
        enum_map[rsid_py.Status.TooManySpoofs] = StatusEnum.TooManySpoofs
        enum_map[rsid_py.Status.NotSupported] = StatusEnum.NotSupported
        return enum_map[val]


class AuthenticateStatusEnum(str, Enum):
    Success = 'AuthenticateStatus.Success'
    NoFaceDetected = 'AuthenticateStatus.NoFaceDetected'
    FaceDetected = 'AuthenticateStatus.FaceDetected'
    NoPersonDetected = 'AuthenticateStatus.NoPersonDetected'
    PersonDetected = 'AuthenticateStatus.PersonDetected'
    BarcodeNotFound = 'AuthenticateStatus.BarcodeNotFound'
    BarcodeFound = 'AuthenticateStatus.BarcodeFound'
    LedFlowSuccess = 'AuthenticateStatus.LedFlowSuccess'
    FaceIsTooFarToTheTop = 'AuthenticateStatus.FaceIsTooFarToTheTop'
    FaceIsTooFarToTheBottom = 'AuthenticateStatus.FaceIsTooFarToTheBottom'
    FaceIsTooFarToTheRight = 'AuthenticateStatus.FaceIsTooFarToTheRight'
    FaceIsTooFarToTheLeft = 'AuthenticateStatus.FaceIsTooFarToTheLeft'
    FaceTiltIsTooUp = 'AuthenticateStatus.FaceTiltIsTooUp'
    FaceTiltIsTooDown = 'AuthenticateStatus.FaceTiltIsTooDown'
    FaceTiltIsTooRight = 'AuthenticateStatus.FaceTiltIsTooRight'
    FaceTiltIsTooLeft = 'AuthenticateStatus.FaceTiltIsTooLeft'
    FaceIsNotFrontal = 'AuthenticateStatus.FaceIsNotFrontal'
    CameraStarted = 'AuthenticateStatus.CameraStarted'
    CameraStopped = 'AuthenticateStatus.CameraStopped'
    Spoof = 'AuthenticateStatus.Spoof'
    Forbidden = 'AuthenticateStatus.Forbidden'
    DeviceError = 'AuthenticateStatus.DeviceError'
    Failure = 'AuthenticateStatus.Failure'
    TooManySpoofs = 'AuthenticateStatus.TooManySpoofs'
    InvalidFeatures = 'AuthenticateStatus.InvalidFeatures'
    Ok = 'AuthenticateStatus.Ok'
    Error = 'AuthenticateStatus.Error'
    SerialError = 'AuthenticateStatus.SerialError'
    SecurityError = 'AuthenticateStatus.SecurityError'
    VersionMismatch = 'AuthenticateStatus.VersionMismatch'
    CrcError = 'AuthenticateStatus.CrcError'
    Spoof_2D = 'AuthenticateStatus.Spoof_2D'
    Spoof_3D = 'AuthenticateStatus.Spoof_3D'
    Spoof_LR = 'AuthenticateStatus.Spoof_LR'
    Spoof_Surface = 'AuthenticateStatus.Spoof_Surface'
    Spoof_Disparity = 'AuthenticateStatus.Spoof_Disparity'
    Spoof_Vision = 'AuthenticateStatus.Spoof_Vision'
    Spoof_2D_Right = 'AuthenticateStatus.Spoof_2D_Right'
    Spoof_Plane_Disparity = 'AuthenticateStatus.Spoof_Plane_Disparity'
    Sunglasses = 'AuthenticateStatus.Sunglasses'
    MedicalMask = 'AuthenticateStatus.MedicalMask'

    def __str__(self):
        return f'{self.value}'

    def to_rsid_py(self) -> rsid_py.AuthenticateStatus:
        enum_map = {}
        enum_map['AuthenticateStatus.Success'] = rsid_py.AuthenticateStatus.Success
        enum_map['AuthenticateStatus.NoFaceDetected'] = rsid_py.AuthenticateStatus.NoFaceDetected
        enum_map['AuthenticateStatus.FaceDetected'] = rsid_py.AuthenticateStatus.FaceDetected
        enum_map['AuthenticateStatus.NoPersonDetected'] = rsid_py.AuthenticateStatus.NoPersonDetected
        enum_map['AuthenticateStatus.PersonDetected'] = rsid_py.AuthenticateStatus.PersonDetected
        enum_map['AuthenticateStatus.BarcodeNotFound'] = rsid_py.AuthenticateStatus.BarcodeNotFound
        enum_map['AuthenticateStatus.BarcodeFound'] = rsid_py.AuthenticateStatus.BarcodeFound
        enum_map['AuthenticateStatus.LedFlowSuccess'] = rsid_py.AuthenticateStatus.LedFlowSuccess
        enum_map['AuthenticateStatus.FaceIsTooFarToTheTop'] = rsid_py.AuthenticateStatus.FaceIsTooFarToTheTop
        enum_map['AuthenticateStatus.FaceIsTooFarToTheBottom'] = rsid_py.AuthenticateStatus.FaceIsTooFarToTheBottom
        enum_map['AuthenticateStatus.FaceIsTooFarToTheRight'] = rsid_py.AuthenticateStatus.FaceIsTooFarToTheRight
        enum_map['AuthenticateStatus.FaceIsTooFarToTheLeft'] = rsid_py.AuthenticateStatus.FaceIsTooFarToTheLeft
        enum_map['AuthenticateStatus.FaceTiltIsTooUp'] = rsid_py.AuthenticateStatus.FaceTiltIsTooUp
        enum_map['AuthenticateStatus.FaceTiltIsTooDown'] = rsid_py.AuthenticateStatus.FaceTiltIsTooDown
        enum_map['AuthenticateStatus.FaceTiltIsTooRight'] = rsid_py.AuthenticateStatus.FaceTiltIsTooRight
        enum_map['AuthenticateStatus.FaceTiltIsTooLeft'] = rsid_py.AuthenticateStatus.FaceTiltIsTooLeft
        enum_map['AuthenticateStatus.FaceIsNotFrontal'] = rsid_py.AuthenticateStatus.FaceIsNotFrontal
        enum_map['AuthenticateStatus.CameraStarted'] = rsid_py.AuthenticateStatus.CameraStarted
        enum_map['AuthenticateStatus.CameraStopped'] = rsid_py.AuthenticateStatus.CameraStopped
        enum_map['AuthenticateStatus.Spoof'] = rsid_py.AuthenticateStatus.Spoof
        enum_map['AuthenticateStatus.Forbidden'] = rsid_py.AuthenticateStatus.Forbidden
        enum_map['AuthenticateStatus.DeviceError'] = rsid_py.AuthenticateStatus.DeviceError
        enum_map['AuthenticateStatus.Failure'] = rsid_py.AuthenticateStatus.Failure
        enum_map['AuthenticateStatus.TooManySpoofs'] = rsid_py.AuthenticateStatus.TooManySpoofs
        enum_map['AuthenticateStatus.InvalidFeatures'] = rsid_py.AuthenticateStatus.InvalidFeatures
        enum_map['AuthenticateStatus.Ok'] = rsid_py.AuthenticateStatus.Ok
        enum_map['AuthenticateStatus.Error'] = rsid_py.AuthenticateStatus.Error
        enum_map['AuthenticateStatus.SerialError'] = rsid_py.AuthenticateStatus.SerialError
        enum_map['AuthenticateStatus.SecurityError'] = rsid_py.AuthenticateStatus.SecurityError
        enum_map['AuthenticateStatus.VersionMismatch'] = rsid_py.AuthenticateStatus.VersionMismatch
        enum_map['AuthenticateStatus.CrcError'] = rsid_py.AuthenticateStatus.CrcError
        enum_map['AuthenticateStatus.Spoof_2D'] = rsid_py.AuthenticateStatus.Spoof_2D
        enum_map['AuthenticateStatus.Spoof_3D'] = rsid_py.AuthenticateStatus.Spoof_3D
        enum_map['AuthenticateStatus.Spoof_LR'] = rsid_py.AuthenticateStatus.Spoof_LR
        enum_map['AuthenticateStatus.Spoof_Surface'] = rsid_py.AuthenticateStatus.Spoof_Surface
        enum_map['AuthenticateStatus.Spoof_Disparity'] = rsid_py.AuthenticateStatus.Spoof_Disparity
        enum_map['AuthenticateStatus.Spoof_Vision'] = rsid_py.AuthenticateStatus.Spoof_Vision
        enum_map['AuthenticateStatus.Spoof_2D_Right'] = rsid_py.AuthenticateStatus.Spoof_2D_Right
        enum_map['AuthenticateStatus.Spoof_Plane_Disparity'] = rsid_py.AuthenticateStatus.Spoof_Plane_Disparity
        enum_map['AuthenticateStatus.Sunglasses'] = rsid_py.AuthenticateStatus.Sunglasses
        enum_map['AuthenticateStatus.MedicalMask'] = rsid_py.AuthenticateStatus.MedicalMask
        return enum_map[self.value]

    @classmethod
    def from_rsid_py(cls, val: rsid_py.AuthenticateStatus) -> 'AuthenticateStatusEnum':
        enum_map = {}
        enum_map[rsid_py.AuthenticateStatus.Success] = AuthenticateStatusEnum.Success
        enum_map[rsid_py.AuthenticateStatus.NoFaceDetected] = AuthenticateStatusEnum.NoFaceDetected
        enum_map[rsid_py.AuthenticateStatus.FaceDetected] = AuthenticateStatusEnum.FaceDetected
        enum_map[rsid_py.AuthenticateStatus.NoPersonDetected] = AuthenticateStatusEnum.NoPersonDetected
        enum_map[rsid_py.AuthenticateStatus.PersonDetected] = AuthenticateStatusEnum.PersonDetected
        enum_map[rsid_py.AuthenticateStatus.BarcodeNotFound] = AuthenticateStatusEnum.BarcodeNotFound
        enum_map[rsid_py.AuthenticateStatus.BarcodeFound] = AuthenticateStatusEnum.BarcodeFound
        enum_map[rsid_py.AuthenticateStatus.LedFlowSuccess] = AuthenticateStatusEnum.LedFlowSuccess
        enum_map[rsid_py.AuthenticateStatus.FaceIsTooFarToTheTop] = AuthenticateStatusEnum.FaceIsTooFarToTheTop
        enum_map[rsid_py.AuthenticateStatus.FaceIsTooFarToTheBottom] = AuthenticateStatusEnum.FaceIsTooFarToTheBottom
        enum_map[rsid_py.AuthenticateStatus.FaceIsTooFarToTheRight] = AuthenticateStatusEnum.FaceIsTooFarToTheRight
        enum_map[rsid_py.AuthenticateStatus.FaceIsTooFarToTheLeft] = AuthenticateStatusEnum.FaceIsTooFarToTheLeft
        enum_map[rsid_py.AuthenticateStatus.FaceTiltIsTooUp] = AuthenticateStatusEnum.FaceTiltIsTooUp
        enum_map[rsid_py.AuthenticateStatus.FaceTiltIsTooDown] = AuthenticateStatusEnum.FaceTiltIsTooDown
        enum_map[rsid_py.AuthenticateStatus.FaceTiltIsTooRight] = AuthenticateStatusEnum.FaceTiltIsTooRight
        enum_map[rsid_py.AuthenticateStatus.FaceTiltIsTooLeft] = AuthenticateStatusEnum.FaceTiltIsTooLeft
        enum_map[rsid_py.AuthenticateStatus.FaceIsNotFrontal] = AuthenticateStatusEnum.FaceIsNotFrontal
        enum_map[rsid_py.AuthenticateStatus.CameraStarted] = AuthenticateStatusEnum.CameraStarted
        enum_map[rsid_py.AuthenticateStatus.CameraStopped] = AuthenticateStatusEnum.CameraStopped
        enum_map[rsid_py.AuthenticateStatus.Spoof] = AuthenticateStatusEnum.Spoof
        enum_map[rsid_py.AuthenticateStatus.Forbidden] = AuthenticateStatusEnum.Forbidden
        enum_map[rsid_py.AuthenticateStatus.DeviceError] = AuthenticateStatusEnum.DeviceError
        enum_map[rsid_py.AuthenticateStatus.Failure] = AuthenticateStatusEnum.Failure
        enum_map[rsid_py.AuthenticateStatus.TooManySpoofs] = AuthenticateStatusEnum.TooManySpoofs
        enum_map[rsid_py.AuthenticateStatus.InvalidFeatures] = AuthenticateStatusEnum.InvalidFeatures
        enum_map[rsid_py.AuthenticateStatus.Ok] = AuthenticateStatusEnum.Ok
        enum_map[rsid_py.AuthenticateStatus.Error] = AuthenticateStatusEnum.Error
        enum_map[rsid_py.AuthenticateStatus.SerialError] = AuthenticateStatusEnum.SerialError
        enum_map[rsid_py.AuthenticateStatus.SecurityError] = AuthenticateStatusEnum.SecurityError
        enum_map[rsid_py.AuthenticateStatus.VersionMismatch] = AuthenticateStatusEnum.VersionMismatch
        enum_map[rsid_py.AuthenticateStatus.CrcError] = AuthenticateStatusEnum.CrcError
        enum_map[rsid_py.AuthenticateStatus.Spoof_2D] = AuthenticateStatusEnum.Spoof_2D
        enum_map[rsid_py.AuthenticateStatus.Spoof_3D] = AuthenticateStatusEnum.Spoof_3D
        enum_map[rsid_py.AuthenticateStatus.Spoof_LR] = AuthenticateStatusEnum.Spoof_LR
        enum_map[rsid_py.AuthenticateStatus.Spoof_Surface] = AuthenticateStatusEnum.Spoof_Surface
        enum_map[rsid_py.AuthenticateStatus.Spoof_Disparity] = AuthenticateStatusEnum.Spoof_Disparity
        enum_map[rsid_py.AuthenticateStatus.Spoof_Vision] = AuthenticateStatusEnum.Spoof_Vision
        enum_map[rsid_py.AuthenticateStatus.Spoof_2D_Right] = AuthenticateStatusEnum.Spoof_2D_Right
        enum_map[rsid_py.AuthenticateStatus.Spoof_Plane_Disparity] = AuthenticateStatusEnum.Spoof_Plane_Disparity
        enum_map[rsid_py.AuthenticateStatus.Sunglasses] = AuthenticateStatusEnum.Sunglasses
        enum_map[rsid_py.AuthenticateStatus.MedicalMask] = AuthenticateStatusEnum.MedicalMask
        return enum_map[val]


class EnrollStatusEnum(str, Enum):
    Success = 'EnrollStatus.Success'
    NoFaceDetected = 'EnrollStatus.NoFaceDetected'
    FaceDetected = 'EnrollStatus.FaceDetected'
    PersonNotFound = 'EnrollStatus.PersonNotFound'
    PersonFound = 'EnrollStatus.PersonFound'
    BarcodeNotFound = 'EnrollStatus.BarcodeNotFound'
    BarcodeFound = 'EnrollStatus.BarcodeFound'
    LedFlowSuccess = 'EnrollStatus.LedFlowSuccess'
    FaceIsTooFarToTheTop = 'EnrollStatus.FaceIsTooFarToTheTop'
    FaceIsTooFarToTheBottom = 'EnrollStatus.FaceIsTooFarToTheBottom'
    FaceIsTooFarToTheRight = 'EnrollStatus.FaceIsTooFarToTheRight'
    FaceIsTooFarToTheLeft = 'EnrollStatus.FaceIsTooFarToTheLeft'
    FaceTiltIsTooUp = 'EnrollStatus.FaceTiltIsTooUp'
    FaceTiltIsTooDown = 'EnrollStatus.FaceTiltIsTooDown'
    FaceTiltIsTooRight = 'EnrollStatus.FaceTiltIsTooRight'
    FaceTiltIsTooLeft = 'EnrollStatus.FaceTiltIsTooLeft'
    FaceIsNotFrontal = 'EnrollStatus.FaceIsNotFrontal'
    CameraStarted = 'EnrollStatus.CameraStarted'
    CameraStopped = 'EnrollStatus.CameraStopped'
    MultipleFacesDetected = 'EnrollStatus.MultipleFacesDetected'
    Failure = 'EnrollStatus.Failure'
    DeviceError = 'EnrollStatus.DeviceError'
    Spoof = 'EnrollStatus.Spoof'
    InvalidFeatures = 'EnrollStatus.InvalidFeatures'
    # Ambiguous  = 'EnrollStatus.Ambiguous '
    Ok = 'EnrollStatus.Ok'
    Error = 'EnrollStatus.Error'
    SerialError = 'EnrollStatus.SerialError'
    SecurityError = 'EnrollStatus.SecurityError'
    VersionMismatch = 'EnrollStatus.VersionMismatch'
    CrcError = 'EnrollStatus.CrcError'
    TooManySpoofs = 'EnrollStatus.TooManySpoofs'
    NotSupported = 'EnrollStatus.NotSupported'
    DatabaseFull = 'EnrollStatus.DatabaseFull'
    DuplicateUserId = 'EnrollStatus.DuplicateUserId'
    Spoof_2D = 'EnrollStatus.Spoof_2D'
    Spoof_3D = 'EnrollStatus.Spoof_3D'
    Spoof_LR = 'EnrollStatus.Spoof_LR'
    Spoof_Surface = 'EnrollStatus.Spoof_Surface'
    Spoof_Disparity = 'EnrollStatus.Spoof_Disparity'
    Spoof_Vision = 'EnrollStatus.Spoof_Vision'
    Spoof_2D_Right = 'EnrollStatus.Spoof_2D_Right'
    Spoof_Plane_Disparity = 'EnrollStatus.Spoof_Plane_Disparity'
    Sunglasses = 'EnrollStatus.Sunglasses'
    MedicalMask = 'EnrollStatus.MedicalMask'

    def __str__(self):
        return f'{self.value}'

    def to_rsid_py(self) -> rsid_py.EnrollStatus:
        enum_map = {}
        enum_map['EnrollStatus.Success'] = rsid_py.EnrollStatus.Success
        enum_map['EnrollStatus.NoFaceDetected'] = rsid_py.EnrollStatus.NoFaceDetected
        enum_map['EnrollStatus.FaceDetected'] = rsid_py.EnrollStatus.FaceDetected
        enum_map['EnrollStatus.PersonNotFound'] = rsid_py.EnrollStatus.PersonNotFound
        enum_map['EnrollStatus.PersonFound'] = rsid_py.EnrollStatus.PersonFound
        enum_map['EnrollStatus.BarcodeNotFound'] = rsid_py.EnrollStatus.BarcodeNotFound
        enum_map['EnrollStatus.BarcodeFound'] = rsid_py.EnrollStatus.BarcodeFound
        enum_map['EnrollStatus.LedFlowSuccess'] = rsid_py.EnrollStatus.LedFlowSuccess
        enum_map['EnrollStatus.FaceIsTooFarToTheTop'] = rsid_py.EnrollStatus.FaceIsTooFarToTheTop
        enum_map['EnrollStatus.FaceIsTooFarToTheBottom'] = rsid_py.EnrollStatus.FaceIsTooFarToTheBottom
        enum_map['EnrollStatus.FaceIsTooFarToTheRight'] = rsid_py.EnrollStatus.FaceIsTooFarToTheRight
        enum_map['EnrollStatus.FaceIsTooFarToTheLeft'] = rsid_py.EnrollStatus.FaceIsTooFarToTheLeft
        enum_map['EnrollStatus.FaceTiltIsTooUp'] = rsid_py.EnrollStatus.FaceTiltIsTooUp
        enum_map['EnrollStatus.FaceTiltIsTooDown'] = rsid_py.EnrollStatus.FaceTiltIsTooDown
        enum_map['EnrollStatus.FaceTiltIsTooRight'] = rsid_py.EnrollStatus.FaceTiltIsTooRight
        enum_map['EnrollStatus.FaceTiltIsTooLeft'] = rsid_py.EnrollStatus.FaceTiltIsTooLeft
        enum_map['EnrollStatus.FaceIsNotFrontal'] = rsid_py.EnrollStatus.FaceIsNotFrontal
        enum_map['EnrollStatus.CameraStarted'] = rsid_py.EnrollStatus.CameraStarted
        enum_map['EnrollStatus.CameraStopped'] = rsid_py.EnrollStatus.CameraStopped
        enum_map['EnrollStatus.MultipleFacesDetected'] = rsid_py.EnrollStatus.MultipleFacesDetected
        enum_map['EnrollStatus.Failure'] = rsid_py.EnrollStatus.Failure
        enum_map['EnrollStatus.DeviceError'] = rsid_py.EnrollStatus.DeviceError
        enum_map['EnrollStatus.Spoof'] = rsid_py.EnrollStatus.Spoof
        enum_map['EnrollStatus.InvalidFeatures'] = rsid_py.EnrollStatus.InvalidFeatures
        # enum_map['EnrollStatus.Ambiguous '] = rsid_py.EnrollStatus.Ambiguous
        enum_map['EnrollStatus.Ok'] = rsid_py.EnrollStatus.Ok
        enum_map['EnrollStatus.Error'] = rsid_py.EnrollStatus.Error
        enum_map['EnrollStatus.SerialError'] = rsid_py.EnrollStatus.SerialError
        enum_map['EnrollStatus.SecurityError'] = rsid_py.EnrollStatus.SecurityError
        enum_map['EnrollStatus.VersionMismatch'] = rsid_py.EnrollStatus.VersionMismatch
        enum_map['EnrollStatus.CrcError'] = rsid_py.EnrollStatus.CrcError
        enum_map['EnrollStatus.TooManySpoofs'] = rsid_py.EnrollStatus.TooManySpoofs
        enum_map['EnrollStatus.NotSupported'] = rsid_py.EnrollStatus.NotSupported
        enum_map['EnrollStatus.DatabaseFull'] = rsid_py.EnrollStatus.DatabaseFull
        enum_map['EnrollStatus.DuplicateUserId'] = rsid_py.EnrollStatus.DuplicateUserId
        enum_map['EnrollStatus.Spoof_2D'] = rsid_py.EnrollStatus.Spoof_2D
        enum_map['EnrollStatus.Spoof_3D'] = rsid_py.EnrollStatus.Spoof_3D
        enum_map['EnrollStatus.Spoof_LR'] = rsid_py.EnrollStatus.Spoof_LR
        enum_map['EnrollStatus.Spoof_Surface'] = rsid_py.EnrollStatus.Spoof_Surface
        enum_map['EnrollStatus.Spoof_Disparity'] = rsid_py.EnrollStatus.Spoof_Disparity
        enum_map['EnrollStatus.Spoof_Vision'] = rsid_py.EnrollStatus.Spoof_Vision
        enum_map['EnrollStatus.Spoof_2D_Right'] = rsid_py.EnrollStatus.Spoof_2D_Right
        enum_map['EnrollStatus.Spoof_Plane_Disparity'] = rsid_py.EnrollStatus.Spoof_Plane_Disparity
        enum_map['EnrollStatus.Sunglasses'] = rsid_py.EnrollStatus.Sunglasses
        enum_map['EnrollStatus.MedicalMask'] = rsid_py.EnrollStatus.MedicalMask
        return enum_map[self.value]

    @classmethod
    def from_rsid_py(cls, val: rsid_py.EnrollStatus) -> 'EnrollStatusEnum':
        enum_map = {}
        enum_map[rsid_py.EnrollStatus.Success] = EnrollStatusEnum.Success
        enum_map[rsid_py.EnrollStatus.NoFaceDetected] = EnrollStatusEnum.NoFaceDetected
        enum_map[rsid_py.EnrollStatus.FaceDetected] = EnrollStatusEnum.FaceDetected
        enum_map[rsid_py.EnrollStatus.PersonNotFound] = EnrollStatusEnum.PersonNotFound
        enum_map[rsid_py.EnrollStatus.PersonFound] = EnrollStatusEnum.PersonFound
        enum_map[rsid_py.EnrollStatus.BarcodeNotFound] = EnrollStatusEnum.BarcodeNotFound
        enum_map[rsid_py.EnrollStatus.BarcodeFound] = EnrollStatusEnum.BarcodeFound
        enum_map[rsid_py.EnrollStatus.LedFlowSuccess] = EnrollStatusEnum.LedFlowSuccess
        enum_map[rsid_py.EnrollStatus.FaceIsTooFarToTheTop] = EnrollStatusEnum.FaceIsTooFarToTheTop
        enum_map[rsid_py.EnrollStatus.FaceIsTooFarToTheBottom] = EnrollStatusEnum.FaceIsTooFarToTheBottom
        enum_map[rsid_py.EnrollStatus.FaceIsTooFarToTheRight] = EnrollStatusEnum.FaceIsTooFarToTheRight
        enum_map[rsid_py.EnrollStatus.FaceIsTooFarToTheLeft] = EnrollStatusEnum.FaceIsTooFarToTheLeft
        enum_map[rsid_py.EnrollStatus.FaceTiltIsTooUp] = EnrollStatusEnum.FaceTiltIsTooUp
        enum_map[rsid_py.EnrollStatus.FaceTiltIsTooDown] = EnrollStatusEnum.FaceTiltIsTooDown
        enum_map[rsid_py.EnrollStatus.FaceTiltIsTooRight] = EnrollStatusEnum.FaceTiltIsTooRight
        enum_map[rsid_py.EnrollStatus.FaceTiltIsTooLeft] = EnrollStatusEnum.FaceTiltIsTooLeft
        enum_map[rsid_py.EnrollStatus.FaceIsNotFrontal] = EnrollStatusEnum.FaceIsNotFrontal
        enum_map[rsid_py.EnrollStatus.CameraStarted] = EnrollStatusEnum.CameraStarted
        enum_map[rsid_py.EnrollStatus.CameraStopped] = EnrollStatusEnum.CameraStopped
        enum_map[rsid_py.EnrollStatus.MultipleFacesDetected] = EnrollStatusEnum.MultipleFacesDetected
        enum_map[rsid_py.EnrollStatus.Failure] = EnrollStatusEnum.Failure
        enum_map[rsid_py.EnrollStatus.DeviceError] = EnrollStatusEnum.DeviceError
        enum_map[rsid_py.EnrollStatus.Spoof] = EnrollStatusEnum.Spoof
        enum_map[rsid_py.EnrollStatus.InvalidFeatures] = EnrollStatusEnum.InvalidFeatures
        # enum_map[rsid_py.EnrollStatus.Ambiguous ] = EnrollStatusEnum.Ambiguous
        enum_map[rsid_py.EnrollStatus.Ok] = EnrollStatusEnum.Ok
        enum_map[rsid_py.EnrollStatus.Error] = EnrollStatusEnum.Error
        enum_map[rsid_py.EnrollStatus.SerialError] = EnrollStatusEnum.SerialError
        enum_map[rsid_py.EnrollStatus.SecurityError] = EnrollStatusEnum.SecurityError
        enum_map[rsid_py.EnrollStatus.VersionMismatch] = EnrollStatusEnum.VersionMismatch
        enum_map[rsid_py.EnrollStatus.CrcError] = EnrollStatusEnum.CrcError
        enum_map[rsid_py.EnrollStatus.TooManySpoofs] = EnrollStatusEnum.TooManySpoofs
        enum_map[rsid_py.EnrollStatus.NotSupported] = EnrollStatusEnum.NotSupported
        enum_map[rsid_py.EnrollStatus.DatabaseFull] = EnrollStatusEnum.DatabaseFull
        enum_map[rsid_py.EnrollStatus.DuplicateUserId] = EnrollStatusEnum.DuplicateUserId
        enum_map[rsid_py.EnrollStatus.Spoof_2D] = EnrollStatusEnum.Spoof_2D
        enum_map[rsid_py.EnrollStatus.Spoof_3D] = EnrollStatusEnum.Spoof_3D
        enum_map[rsid_py.EnrollStatus.Spoof_LR] = EnrollStatusEnum.Spoof_LR
        enum_map[rsid_py.EnrollStatus.Spoof_Surface] = EnrollStatusEnum.Spoof_Surface
        enum_map[rsid_py.EnrollStatus.Spoof_Disparity] = EnrollStatusEnum.Spoof_Disparity
        enum_map[rsid_py.EnrollStatus.Spoof_Vision] = EnrollStatusEnum.Spoof_Vision
        enum_map[rsid_py.EnrollStatus.Spoof_2D_Right] = EnrollStatusEnum.Spoof_2D_Right
        enum_map[rsid_py.EnrollStatus.Spoof_Plane_Disparity] = EnrollStatusEnum.Spoof_Plane_Disparity
        enum_map[rsid_py.EnrollStatus.Sunglasses] = EnrollStatusEnum.Sunglasses
        enum_map[rsid_py.EnrollStatus.MedicalMask] = EnrollStatusEnum.MedicalMask
        return enum_map[val]



